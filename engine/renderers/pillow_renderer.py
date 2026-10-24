from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parents[2]
OUT_DIR = BASE_DIR / "output" / "comics"
ART_PATH = BASE_DIR / "assets" / "story-art" / "tortoise-hare-comic-art.png"

STORIES = {
    "en": {
        "title": "The Tortoise and the Hare",
        "hello": "Hello, friend!",
        "reply": "Hello! How are you?",
        "boast": "I can run much faster than you!",
        "challenge": "Let's have a race!",
        "race": "The race began. The tortoise kept walking, one step at a time.",
        "nap": "The hare felt sure he would win, so he stopped for a nap.",
        "finish": "The tortoise kept going and won. Slow and steady can win the race!",
        "surprise": "Oh no! You won!",
    },
    "kn": {
        "title": "ಆಮೆ ಮತ್ತು ಮೊಲ",
        "hello": "ನಮಸ್ಕಾರ, ಗೆಳೆಯಾ!",
        "reply": "ನಮಸ್ಕಾರ! ನೀನು ಹೇಗಿದ್ದೀಯ?",
        "boast": "ನಾನು ನಿನಗಿಂತ ವೇಗವಾಗಿ ಓಡಬಲ್ಲೆ!",
        "challenge": "ಒಂದು ಓಟ ನಡೆಸೋಣ!",
        "race": "ಓಟ ಆರಂಭವಾಯಿತು. ಆಮೆ ಒಂದೊಂದೇ ಹೆಜ್ಜೆ ಇಡುತ್ತಾ ಸಾಗಿತು.",
        "nap": "ತಾನೇ ಗೆಲ್ಲುತ್ತೇನೆ ಎಂದುಕೊಂಡ ಮೊಲ ನಿದ್ರೆ ಮಾಡಲು ನಿಂತಿತು.",
        "finish": "ಆಮೆ ನಿಲ್ಲದೆ ಸಾಗಿತು ಮತ್ತು ಗೆದ್ದಿತು. ನಿಧಾನವಾದರೂ ನಿರಂತರವಾಗಿ ಸಾಗು!",
        "surprise": "ಅಯ್ಯೋ! ನೀನು ಗೆದ್ದೆ!",
    },
}

def load_font(size, bold=False, kannada=False):
    candidates = []
    if kannada:
        candidates.extend([
            "/usr/share/fonts/truetype/noto/NotoSansKannada-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansKannadaUI-Regular.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansKannada-Regular.ttf",
        ])
    if bold:
        candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    else:
        candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

    for filename in candidates:
        if Path(filename).is_file():
            try:
                return ImageFont.truetype(
                    filename, size, layout_engine=ImageFont.Layout.RAQM
                )
            except Exception:
                return ImageFont.truetype(filename, size)

    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""

    for word in words:
        candidate = word if not current else current + " " + word
        width = draw.textbbox((0, 0), candidate, font=font)[2]

        if width <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_fitted_text(draw, text, box, language, max_size=25,
                     min_size=13, bold=False, color="#26352c",
                     padding=15, line_gap=5):
    x1, y1, x2, y2 = box
    available_width = x2 - x1 - 2 * padding
    available_height = y2 - y1 - 12
    is_kn = language == "kn"

    for size in range(max_size, min_size - 1, -1):
        font = load_font(size, bold=bold, kannada=is_kn)
        lines = wrap_text(draw, text, font, available_width)

        heights = [
            draw.textbbox((0, 0), line, font=font)[3]
            - draw.textbbox((0, 0), line, font=font)[1]
            for line in lines
        ]
        total_height = sum(heights) + line_gap * max(0, len(lines) - 1)

        if total_height <= available_height:
            break
    else:
        font = load_font(min_size, bold=bold, kannada=is_kn)
        lines = wrap_text(draw, text, font, available_width)
        heights = [
            draw.textbbox((0, 0), line, font=font)[3]
            - draw.textbbox((0, 0), line, font=font)[1]
            for line in lines
        ]
        total_height = sum(heights) + line_gap * max(0, len(lines) - 1)

    # Keep all text centred and inside the supplied box.
    y = y1 + max(5, (y2 - y1 - total_height) // 2)

    for line, height in zip(lines, heights):
        draw.text(
            ((x1 + x2) // 2, y),
            line,
            font=font,
            fill=color,
            anchor="mt",
            stroke_width=0,
        )
        y += height + line_gap


def render_comic(language="en"):
    language = "kn" if language == "kn" else "en"

    if not ART_PATH.is_file():
        raise FileNotFoundError(f"Artwork not found: {ART_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    story = STORIES[language]

    with Image.open(ART_PATH) as source:
        image = source.convert("RGB")

    draw = ImageDraw.Draw(image)

    # Coordinates match the 1024 x 1536 comic-page artwork.
    # The text is drawn only inside the blank boxes.
    draw_fitted_text(
        draw, story["title"], (40, 28, 987, 101),
        language, max_size=34, min_size=20, bold=True
    )

    # Opening panel: two characters greeting each other.
    draw_fitted_text(
        draw, story["hello"], (345, 143, 535, 210),
        language, max_size=23, min_size=14, bold=True
    )
    draw_fitted_text(
        draw, story["reply"], (700, 163, 915, 250),
        language, max_size=22, min_size=14, bold=True
    )

    # Challenge panel: the hare boasts and proposes a race.
    draw_fitted_text(
        draw, story["boast"], (140, 464, 405, 523),
        language, max_size=20, min_size=13, bold=True
    )
    draw_fitted_text(
        draw, story["challenge"], (310, 543, 485, 625),
        language, max_size=19, min_size=13, bold=True
    )

    # Narration boxes for the race, nap and finish scenes.
    draw_fitted_text(
        draw, story["race"], (545, 464, 983, 506),
        language, max_size=17, min_size=12
    )
    draw_fitted_text(
        draw, story["nap"], (45, 842, 460, 888),
        language, max_size=18, min_size=12
    )
    draw_fitted_text(
        draw, story["finish"], (45, 1137, 500, 1185),
        language, max_size=18, min_size=12
    )

    # Last speech bubble.
    draw_fitted_text(
        draw, story["surprise"], (850, 1150, 980, 1220),
        language, max_size=18, min_size=12, bold=True
    )

    filename = f"tortoise-and-hare-{language}.png"
    output_path = OUT_DIR / filename
    image.save(output_path, optimize=True)

    return str(output_path)
