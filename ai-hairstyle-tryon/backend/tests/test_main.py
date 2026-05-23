import base64
import io
import json
import os
import sys
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, TryOnRequest, get_image_from_base64
from prompts import PRESETS

client = TestClient(app)

def create_dummy_image_base64() -> str:
    """Creates a tiny 1x1 dummy image and returns its base64."""
    img = Image.new("RGB", (1, 1), color="red")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def test_image_downscaling():
    """Ensure the backend utility correctly resizes and encodes/decodes images without corruption."""
    # Create a 2000x2000 image
    img = Image.new("RGB", (2000, 2000), color="blue")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # decode
    decoded_img = get_image_from_base64(b64_str)
    assert decoded_img.size == (2000, 2000)
    
    # simulate downscale
    decoded_img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    assert decoded_img.size == (1024, 1024)

def test_prompt_builder():
    """Verify that passing 'neon_mohawk' correctly retrieves the exact configured prompt string."""
    preset = PRESETS.get("neon_mohawk")
    assert preset is not None
    assert "mohawk" in preset["image_prompt"].lower()
    assert preset["name"] == "Neon Mohawk"

def test_json_schema_validation():
    """Ensure the TryOnRequest strictly rejects invalid preset_id values."""
    img_b64 = create_dummy_image_base64()
    
    # This should fail due to invalid preset
    response = client.post("/api/tryon", json={
        "image": img_b64,
        "preset_id": "invalid_preset"
    })
    
    assert response.status_code == 422  # Pydantic validation error

@patch("main._create_client")
def test_tryon_api_success(mock_create_client):
    """
    Integration test: Send a dummy base64 string and a valid preset.
    MOCK the google-genai SDK client.models.generate_content methods.
    Verify the endpoint returns 200 OK.
    """
    img_b64 = create_dummy_image_base64()
    
    mock_genai_client = MagicMock()
    mock_create_client.return_value = mock_genai_client
    
    # We need to mock generate_content to return different things based on the model.
    # Since they are called in separate threads, we'll configure a side_effect.
    def mock_generate_content(model, contents, config, **kwargs):
        mock_resp = MagicMock()
        if model == "gemini-3.1-flash-image-preview":
            # Return an image byte mock
            mock_part = MagicMock()
            mock_part.inline_data.data = base64.b64decode(img_b64)
            mock_resp.candidates = [MagicMock(content=MagicMock(parts=[mock_part]))]
        elif model == "gemini-3.5-flash":
            # Return JSON string
            mock_resp.text = json.dumps({
                "stylist_note": "A sassy note.",
                "vibe_rating": "10/10"
            })
        return mock_resp
        
    mock_genai_client.models.generate_content.side_effect = mock_generate_content
    
    response = client.post("/api/tryon", json={
        "image": f"data:image/png;base64,{img_b64}",
        "preset_id": "classic_bangs"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "transformed_image" in data
    assert data["transformed_image"].startswith("data:image/png;base64,")
    assert data["stylist_note"] == "A sassy note."
    assert data["vibe_rating"] == "10/10"
