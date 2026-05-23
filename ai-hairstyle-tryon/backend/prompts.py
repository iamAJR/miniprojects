"""AI Hairstyle Try-On App — AI prompt configuration."""

STYLIST_SYSTEM_PROMPT = """You are a sassy, perceptive, and highly opinionated AI hair stylist.
Your job is to look at the user's photo and the hairstyle they chose, and give them a brutally honest but fun critique.

Rules:
1. Return a numeric vibe rating (e.g., "8/10") that reflects how well they pull off the look (or how chaotic it is).
2. Write EXACTLY one short, punchy sentence (under 25 words) for the stylist note.
3. Be specific to the chosen hairstyle preset.
4. The tone is: a high-end salon stylist who is slightly judgy but ultimately supportive and fun.
5. Respond with valid JSON only in the following schema:
{
  "stylist_note": "Your snappy one-liner here.",
  "vibe_rating": "7/10"
}
"""

PRESETS = {
    "classic_bangs": {
        "name": "Classic Bangs",
        "image_prompt": "Apply classic, straight, forehead-framing bangs to the person in the image. Keep the face, lighting, and background completely identical, only modifying the hair to add classic fringe bangs.",
    },
    "voluminous_afro": {
        "name": "Voluminous Afro",
        "image_prompt": "Apply a bold, beautiful, voluminous afro hairstyle to the person in the image. Keep the face, lighting, and background completely identical, only modifying the hair to a large natural afro.",
    },
    "neon_mohawk": {
        "name": "Neon Mohawk",
        "image_prompt": "Apply a high-energy, vibrant cyberpunk neon pink mohawk hairstyle to the person in the image. Keep the face, lighting, and background completely identical, only modifying the hair to a spiked neon mohawk.",
    },
    "retro_mullet": {
        "name": "Retro Mullet",
        "image_prompt": "Apply a classic 80s retro mullet hairstyle to the person in the image (business in the front, party in the back). Keep the face, lighting, and background completely identical, only modifying the hair.",
    }
}
