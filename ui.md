# AI Hairstyle Try-On App — UX Design Doc

**Designer:** Antigravity (UX)
**Status:** Draft v0.1
**Last updated:** May 2026

---

## 1. The design bet

We're betting that the transition state (the magical loading animation) and the immediate visual comparison carry the entire emotional weight of the product. Therefore, we're spending 80% of our design effort on making the input-to-result transition feel like a premium, playful salon experience, keeping the rest of the interface brutally minimal.

## 2. The defining interaction

User selects a preset (e.g., "Classic Bangs") and taps "Try it on". The button presses down firmly. The input pane slides away, replaced by an obsidian overlay where neon-violet scissors snip and a hair dryer blows softly. After exactly ~3-5s, the screen wipes horizontally to reveal the split "before" and "after" portrait, accompanied by a popping glassmorphic card delivering the "Vibe Rating" and a sassy stylist note. Feels like: getting spun around in a salon chair to face the mirror.

## 3. Screen inventory

- **Home (Input & Presets)** — The single screen where users upload/capture their selfie and pick a style.
- **Result (The Reveal)** — The state showing the side-by-side comparison and the stylist's note.

*(Note: The Loading State exists as a full-screen overlay between these two states.)*

## 4. Screen-by-screen specs

### Home (Input & Presets)

**Purpose:** Get a clear selfie and a hairstyle selection with zero friction.

**Layout (top to bottom):**
1. **Header:** Minimal text logo ("Glow Up") in a stylized, modern font.
2. **Camera/Upload Pane:** A large, central rounded rectangle. Shows live webcam feed by default (if permitted) or a drag-and-drop prompt.
3. **Capture/Upload Button:** A primary neon-accented button overlapping the bottom edge of the pane.
4. **Preset Grid (4 Cards):** A 2x2 grid of beautifully illustrated hairstyle icons (Bangs, Afro, Mohawk, Mullet) acting as radio buttons.
5. **Action Button:** "Try it on" (disabled until an image and a preset are selected).

**Key interactions:**
- Tap "Capture" → Webcam feed pauses, flashes white, and holds the image.
- Tap a Preset card → Card glows with a violet border; other cards dim slightly.
- Tap "Try it on" → Triggers the loading overlay.

**States:**
- **Default:** Camera pane waiting for permission, presets visible but action button disabled.
- **Empty / first-time:** Prompting for camera access or "Upload a photo".
- **Loading:** The defining interaction overlay (scissors/dryer animation).
- **Error:** If camera is denied, falls back to a prominent "Upload Photo" block. If API fails, a soft toast: "The stylist dropped their scissors. Try again."

### Result (The Reveal)

**Purpose:** Deliver the magic moment (the transformation) and the punchline (the stylist note).

**Layout (top to bottom):**
1. **Header:** Minimal text logo.
2. **Comparison Stage:** A large side-by-side (or slider-based) image component taking up 50% of the viewport. Original selfie on left, new style on right.
3. **Vibe Rating & Note Card:** A glowing glassmorphic card floating below the images.
   - **Top:** Huge stylized number (e.g., "8/10").
   - **Body:** The sassy AI stylist note text.
4. **Action Button:** "Try Another Style" (secondary button style).

**Key interactions:**
- Tap "Try Another Style" → Instantly resets the UI back to the Home state, retaining the original selfie but clearing the preset selection.

**States:**
- **Default:** The loaded result.
- **Edge:** Extremely long stylist note (capped by backend, but UI uses a scrollable text area if it overflows).

## 5. The user journey

User opens the web app. The screen is dark, premium, and focused. The central pane asks for camera access; they accept, and see themselves on screen. They adjust their lighting and tap "Capture." The screen flashes, locking their photo in place.
They scroll down slightly to the 4 presets and tap "Neon Mohawk." The card lights up. They tap the now-active "Try it on" button. The UI dims, and playful neon scissors snip across the screen while a hair dryer icon pulses. Three seconds later, the screen wipes to reveal their face rocking a bright pink mohawk. Below it, a glowing card reads: "9/10. Ready for a cyberpunk rave, assuming you survive the commute." They laugh, screenshot the entire page, and immediately tap "Try Another Style."

## 6. Component & visual notes

- **Typography:** Display titles in 'Outfit' or 'Syne' (wide, modern, slightly edgy). Body in 'Inter'.
- **Color:** Deep obsidian background (`#0D0D12`). Accents in electric violet and lavender. Text in off-white.
- **Motion:** Everything uses spring physics. The UI doesn't snap; it glides. The image comparison slider (if used) has a satisfying magnetic drag.
- **The signature visual:** The glowing glassmorphic card for the stylist note. It has a subtle backdrop-filter blur and a slowly shifting gradient border that makes it feel like an expensive, magical object.
- **Microcopy voice:** Confident, sassy, slightly detached. "The stylist is evaluating your choices..."

## 7. Accessibility & inclusion

- High contrast text against the dark background.
- Semantic HTML tags for the image comparison so screen readers can announce "Before image" and "After image".
- Generous tap targets (min 48x48) for the preset grid and capture buttons.
- *Deferred to v2:* Localization (English only for now).

## 8. What we are NOT designing

- **No settings screen** — there is nothing to configure.
- **No gallery/history view** — the magic is in the ephemeral moment.
- **No social sharing buttons** — native screenshots are standard behavior.
- **No cropping/editing tools** — users must capture a good framing initially.
- **No loader progress bars** — progress bars feel like work. We use an animation loop.

## 9. Open design questions

- [ ] Do we use a side-by-side layout for the comparison, or an interactive slider (drag left/right to reveal)? Side-by-side is easier to screenshot in one go.
- [ ] How do we ensure the webcam preview isn't distorted on weird aspect ratio devices?

## 10. Handoff to engineering

The transition from the loading animation to the Result screen is the moment of magic — the wipe effect needs to be 60fps and perfectly synchronized with the image loading. Ensure the generated image is fully pre-fetched before dismissing the loading overlay so there's no layout shift or blank image flash.
