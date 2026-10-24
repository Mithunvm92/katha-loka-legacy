# Katha Loka — visual refresh

A small Flask + Pillow starter for the Katha Loka story studio. The landing page uses a restrained sage-green, warm cream, muted yellow palette and a story-card layout. The comic renderer creates five vertically stacked story scenes for English or Kannada.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# WSL/macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5055. Select English or Kannada and click Create story.

Notes: the illustrations are simple Pillow-drawn placeholders, not production-quality character artwork. Kannada font availability depends on the local machine; install Noto Sans Kannada for best rendering. The Google Fonts import is optional; the page has system fallbacks.
