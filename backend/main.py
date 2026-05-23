"""AI Hairstyle Try-On App — Backend Server."""

import asyncio
import base64
import io
import json
import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel

from prompts import PRESETS, STYLIST_SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="Glow Up - AI Hairstyle Try-On")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use synchronous client for genai (we'll run it in a thread pool for async behavior)
def _create_client():
    """Create a fresh Gemini client for each request."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    # Fallback to vertexai if configured
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

class TryOnRequest(BaseModel):
    image: str
    preset_id: Literal["classic_bangs", "voluminous_afro", "neon_mohawk", "retro_mullet"]

class TryOnResponse(BaseModel):
    transformed_image: str
    stylist_note: str
    vibe_rating: str

def get_image_from_base64(b64_str: str) -> Image.Image:
    """Decodes a base64 string (with or without data URI prefix) into a PIL Image."""
    if "," in b64_str:
        b64_str = b64_str.split(",")[1]
    image_data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(image_data))

def get_image_part(image: Image.Image) -> types.Part:
    """Converts a PIL Image into a google-genai SDK types.Part object."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return types.Part.from_bytes(data=buffered.getvalue(), mime_type="image/png")

def call_image_model(client: genai.Client, image_part: types.Part, preset_id: str) -> str:
    """Calls the image generation model and returns the base64 transformed image."""
    preset_prompt = PRESETS[preset_id]["image_prompt"]
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=[preset_prompt, image_part],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            temperature=0.7,
        ),
    )
    
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            # We have the raw bytes in inline_data.data
            return base64.b64encode(part.inline_data.data).decode("utf-8")
        elif hasattr(part, 'as_image'):
            # Fallback if as_image is available but not inline_data.data directly
            img = part.as_image()
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
            
    raise ValueError("No image returned from Gemini image model.")

def call_text_model(client: genai.Client, image_part: types.Part, preset_id: str) -> dict:
    """Calls the text evaluation model and returns the parsed JSON dict."""
    preset_name = PRESETS[preset_id]["name"]
    user_prompt = f"The user has chosen to try on the '{preset_name}' hairstyle. Evaluate their look."
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            STYLIST_SYSTEM_PROMPT + "\n\n" + user_prompt,
            image_part
        ],
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
        ),
    )
    
    response_text = response.text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
    return json.loads(response_text)

LOCAL_MOCK_RESPONSES = {
    "neon_mohawk": {
        "stylist_note": "Sweetie, this cyberpunk neon mohawk is giving 'I hack mainframes for breakfast' and honestly, I'm here for the absolute chaos. 💅",
        "vibe_rating": "8.5/10"
    },
    "voluminous_afro": {
        "stylist_note": "A bold, majestic statement! The sheer volume is serving pure royalty. Step aside, commoners, a star has entered the salon. ✨",
        "vibe_rating": "9.5/10"
    },
    "classic_bangs": {
        "stylist_note": "Ah, fringe benefits! This classic forehead framer is clean, sophisticated, and slightly mysterious. Very French-chic, darling. ☕",
        "vibe_rating": "9.0/10"
    },
    "retro_mullet": {
        "stylist_note": "Business in the front, absolute lawless party in the back! You are single-handedly bringing the 80s back and I'm legally obligated to love it. 🍻",
        "vibe_rating": "7.5/10"
    }
}

def create_fallback_image(image: Image.Image, preset_id: str) -> str:
    """Creates a stylized mock transformation image when the Gemini Image model is rate-limited on Free Tier."""
    img_copy = image.copy().convert("RGBA")
    overlay = Image.new("RGBA", img_copy.size, (0, 0, 0, 0))
    w, h = img_copy.size
    
    if preset_id == "neon_mohawk":
        # Pink/purple neon tint overlay at the top (hair area)
        for x in range(w):
            for y in range(h):
                if y < h * 0.4:
                    overlay.putpixel((x, y), (255, 0, 128, 120))
    elif preset_id == "voluminous_afro":
        # Golden halo tint at the top
        for x in range(w):
            for y in range(h):
                if y < h * 0.4:
                    overlay.putpixel((x, y), (218, 165, 32, 100))
    elif preset_id == "classic_bangs":
        # Soft dark brown fringe tint
        for x in range(w):
            for y in range(h):
                if y < h * 0.35:
                    overlay.putpixel((x, y), (101, 67, 33, 140))
    elif preset_id == "retro_mullet":
        # Vintage 80s neon green party tint on the back/sides
        for x in range(w):
            for y in range(h):
                if y > h * 0.3:
                    overlay.putpixel((x, y), (57, 255, 20, 80))
                    
    combined = Image.alpha_composite(img_copy, overlay).convert("RGB")
    buffered = io.BytesIO()
    combined.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@app.post("/api/tryon", response_model=TryOnResponse)
async def tryon(request: TryOnRequest):
    """Generate a hairstyle transformation and stylist note concurrently."""
    try:
        if request.preset_id not in PRESETS:
            raise HTTPException(status_code=400, detail="Invalid preset_id")
            
        pil_image = get_image_from_base64(request.image)
        # Downscale if necessary (max 1024x1024)
        pil_image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        image_part = get_image_part(pil_image)
        
        client = _create_client()
        
        # Run synchronous SDK calls in thread pool
        image_task = asyncio.to_thread(call_image_model, client, image_part, request.preset_id)
        text_task = asyncio.to_thread(call_text_model, client, image_part, request.preset_id)
        
        try:
            # Attempt real generation concurrently
            transformed_b64, text_data = await asyncio.gather(image_task, text_task)
        except Exception as e:
            # If the image generation hits a quota exhaustion, fall back to our stylized mockup filter
            # and salvage the high-quality text evaluation from gemini-3.5-flash which is free!
            print(f"Gemini API rate limit or error (running fallbacks): {e}")
            
            # 1. Fallback for the image
            transformed_b64 = create_fallback_image(pil_image, request.preset_id)
            
            # 2. Fallback for the text
            try:
                text_data = await text_task
                text_data["stylist_note"] = text_data.get("stylist_note", "") + " (Note: Using stylist sketch overlay due to Gemini Image Free Tier limits)."
            except Exception as text_err:
                # If BOTH models fail (due to API key rate limits, like 5 RPM on Gemini 3.5 Flash), use our local sassy critiques!
                print(f"Text model failed as well: {text_err}")
                mock_res = LOCAL_MOCK_RESPONSES[request.preset_id]
                text_data = {
                    "stylist_note": mock_res["stylist_note"] + " (Note: Stylist backup sketch & pre-logged critique activated due to Gemini Free Tier rate limits).",
                    "vibe_rating": mock_res["vibe_rating"]
                }
        
        return TryOnResponse(
            transformed_image=f"data:image/png;base64,{transformed_b64}",
            stylist_note=text_data.get("stylist_note", "No comment."),
            vibe_rating=text_data.get("vibe_rating", "?/10")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during tryon generation: {e}")
        raise HTTPException(status_code=500, detail="The stylist is on break. Try another photo.")

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "fabulous"}

# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
