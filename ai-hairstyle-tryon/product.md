# AI Hairstyle Try-On App — Product Design Doc

**Author:** Antigravity (PM)
**Status:** Draft v0.1
**One-liner:** Snap a selfie and instantly see yourself rocking one of four wild hairstyles with a sassy stylist rating.

---

## 1. The user & the moment

- **Who:** Someone curious about changing their look but too intimidated (or broke) to actually go to a salon.
- **When:** Late at night, feeling bored with their appearance, wanting a quick laugh or a genuine "what if" moment.
- **Why now:** AI image editing is finally fast and realistic enough to do this instantly without a heavy app download.

## 2. The contract (I/O)

- **Input:** A live webcam capture or a single uploaded selfie, plus selecting 1 of 4 fixed hairstyle presets.
- **Output:** A side-by-side "before and after" image comparison, delivered with a fun "vibe rating" and a sassy stylist note.
- **The loop:** Open app → capture/upload selfie → pick style → enjoy the loading animation → get the result. Single-shot, no accounts needed.

## 3. The magical moment

> "OMG, that's actually me with bangs! I look ridiculous, but kinda amazing?"

## 4. Scope: what we ARE building (v1)

- A single, responsive web page with a sleek, premium salon aesthetic.
- A unified input pane that supports both file upload and live webcam capture.
- A grid of exactly 4 curated hairstyle presets.
- A fun, salon-themed loading animation (e.g., snipping scissors, blowing dryer) that builds anticipation.
- A final side-by-side result view showing the edited image, a numeric vibe rating, and a sassy stylist note.
- Lightning-fast image transformation using `gemini-3.1-flash-image-preview`.

## 5. Scope: what we are NOT building

- **No user accounts or login** — zero friction to try it once.
- **No session history or galleries** — it's ephemeral; users can screenshot if they want to save it.
- **No styling options beyond the 4 presets** — keeps the UI simple and guarantees high-quality prompt tuning.
- **No custom typed prompts** — prevents abuse and keeps the experience tight.
- **No save/share buttons** — native OS screenshots are good enough for v1.
- **No outfits or background changes** — hairstyles only to ensure the magic works on the face.

## 6. The signature detail

The **Sassy Stylist Note** + **Loading Animation**. As the AI processes, a bouncy, animated pair of scissors and a hair dryer blow across the screen. When the result drops, it doesn't just show the photo—it includes a brutally honest but fun note from an AI stylist (e.g., "7/10. The bangs say 'mysterious art student', but the eyes say 'I need coffee'.")

## 7. Success: how we know it worked

- **Primary:** ≥60% of users who complete their first try-on immediately click to try a second style on the same selfie.
- **Secondary:** High screenshot rate (inferred by repeat usage).
- **What we're NOT measuring:** Total signups, DAU, retention.

## 8. Open questions

- [ ] Can `gemini-3.1-flash-image-preview` consistently keep the original face recognizable while drastically changing the hair?
- [ ] How do we ensure the webcam capture works smoothly across both mobile and desktop browsers?

## 9. Handoff

- **For UX:** The salon-themed loading animation is the bridge to the magic—it needs to feel fun and fast, not like a spinning beach ball.
- **For Eng:** Processing both the image transformation and the stylist text generation concurrently is the key to keeping latency low.
