# Glow Up — AI Hairstyle Try-On App 🌟

A premium single-page web application that lets users try on bold, expressive new hairstyles (like Mohawks, Afros, Bangs, and Mullets) with real-time camera capture or file uploads, paired with highly entertaining, sassy AI-powered stylist evaluations.

---

## 📖 Table of Contents
1. [What This App Does](#what-this-app-does)
2. [Gemini Free Tier Limitations & Fallbacks](#gemini-free-tier-limitations--fallbacks)
3. [Design Docs (Source of Truth)](#design-docs-source-of-truth)
4. [Installation & Setup](#installation--setup)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [What You Learned (Key Takeaways)](#what-you-learned-key-takeaways)

---

## 🧐 What This App Does
**Glow Up** is designed to create a "magical moment" of visual transformation:
* **Webcam & File Upload:** Seamlessly capture a live selfie or upload an existing image.
* **4 Signature Presets:** Instantly try on *Classic Bangs*, *Voluminous Afro*, *Neon Mohawk*, or a *Retro Mullet*.
* **Parallel Gemini Engines:** Concurrently triggers an image-to-image transformation (`gemini-3.1-flash-image-preview`) and a sassy stylist critique engine (`gemini-3.5-flash`).
* **Sassy Feedback:** Get a brutal-but-fun, judgy-but-supportive rating (e.g. `7.5/10`) and a quick salon-style critique.
* **Scissors & Dryer Loading Animation:** A custom CSS micro-animation of clipping scissors and a blowing hair dryer keeps the interface interactive during generation.

---

## ⚠️ Gemini Free Tier Limitations & Fallbacks
> [!IMPORTANT]
> Because your API key is on the Free Tier, Google blocks the actual Gemini image model (`gemini-3.1-flash-image-preview`) completely (its daily limit is literally **0 requests**).
> 
> Because the real AI model is blocked by Google on your free key, the backend is prevented from running the hairstyle generator directly.

### Our Bulletproof Fallback Solution 🛡️
To guarantee an awesome, fully interactive developer and user experience without financial costs, we implemented a **Dual-Layer Fallback System** in the backend:
1. **Visual Sketch Overlays:** If the image model fails with a `429` quota block, the backend uses `PIL` (Python Imaging Library) to construct a custom, stylized neon-color hair filter overlay (specifically tinted for each preset) directly over your uploaded selfie!
2. **Crash-Proof Critique Vault:** The Gemini text model (`gemini-3.5-flash`) has a strict **5 requests-per-minute** rate limit on free keys. If you click through presets too quickly and hit a rate limit, the backend automatically falls back to a curated database of custom, highly sassy salon-style critiques so the app **never crashes** and stays responsive!

---

## 🎯 Design Docs (Source of Truth)
We adhered strictly to three product and engineering specifications generated during the planning phase. These remain the **absolute source of truth** for understanding the app's structure, styling, and code guidelines:
* 📄 [product.md](product.md) — Product requirements, MVP scope, core features, and sassy tone.
* 📄 [ui.md](ui.md) — Visual styles, dark-theme guidelines, Outfit/Inter typography, and glassmorphic designs.
* 📄 [engineering.md](engineering.md) — Backend architecture, parallel SDK execution model, endpoint definitions, and testing strategies.

---

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.12+**
* **Astral `uv`** (modern, ultra-fast Python package manager)

### Step 1: Install Dependencies
Navigate to the `backend` folder and sync the virtual environment using `uv`:
```bash
cd backend
uv sync
```
This automatically sets up a `.venv` virtual environment and installs all dependencies listed in `pyproject.toml` (including `fastapi`, `google-genai`, `Pillow`, `pytest`, and `python-dotenv`).

### Step 2: Environment Variables
Create a `.env` file inside the `backend` folder:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 Running the Application

Start the FastAPI application served locally:
```bash
cd backend
uv run uvicorn main:app --reload
```

Open your browser and visit:
👉 **[http://localhost:8000](http://localhost:8000)**

*The FastAPI backend serves the frontend single-page app statically at the root (`/`)!*

---

## 🧪 Testing

We built a robust test suite covering downscaling utilities, prompt builders, schema validations, and mock Gemini API calls. Run the tests from the `backend/` directory:
```bash
cd backend
PYTHONPATH=. .venv/bin/pytest -v
```

---

## 🎓 What You Learned (Key Takeaways)

Here is a summary of the powerful software engineering principles and workflows you mastered during this workshop:

| Skill | Why It Matters |
| :--- | :--- |
| **Spec → Code+Test → Verify** | Plan first. Build code and tests together. Click around last. Always in that order. |
| **Fix the doc, not the code** | When something's off, change the plan and rebuild. Don't patch. |
| **Tests as a safety gate** | Built into implementation — AI catches the dumb stuff before you have to. |
| **The regression rule** | Every human-found bug becomes a test. The bug can never come back. |
| **Doc-driven pivots** | When direction changes, change the doc — AI handles the rest. |
| **Antigravity 3-layer flow** | English in chat → agent picks command → you approve. |

---

*Made with 💜 during the Coding Jam. Keep glowing up!*
