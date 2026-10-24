from pathlib import Path

from flask import Flask, render_template, request, url_for, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"
OUTPUT_DIR = BASE_DIR / "output" / "comics"

TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
)

ALLOWED_LANGUAGES = {"en", "kn"}
ALLOWED_COMICS = {
    "tortoise-and-hare-en.png",
    "tortoise-and-hare-kn.png",
}


@app.route("/", methods=["GET", "POST"])
def index():
    language = "en"
    message = ""
    comic_url = None

    if request.method == "POST":
        language = request.form.get("language", "en")
        if language not in ALLOWED_LANGUAGES:
            language = "en"

        try:
            from engine.renderers.pillow_renderer import render_comic

            result = render_comic(language)
            filename = Path(result).name
            if filename not in ALLOWED_COMICS:
                raise ValueError("Unexpected comic output filename")

            comic_url = url_for("comic_file", filename=filename)
            message = "Your comic is ready!"
        except Exception:
            app.logger.exception("Comic generation failed")
            message = (
                "Comic generation failed. Check the terminal logs "
                "for the exact error."
            )

    return render_template(
        "index.html",
        language=language,
        comic_url=comic_url,
        message=message,
    )


@app.route("/reader")
def reader():
    language = request.args.get("language", "en")
    if language not in ALLOWED_LANGUAGES:
        language = "en"

    comic_filename = (
        "tortoise-and-hare-kn.png"
        if language == "kn"
        else "tortoise-and-hare-en.png"
    )

    return render_template(
        "reader.html",
        language=language,
        comic_filename=comic_filename,
    )


@app.route("/comics/<path:filename>")
def comic_file(filename):
    if filename not in ALLOWED_COMICS:
        return "Comic not found", 404

    file_path = OUTPUT_DIR / filename
    if not file_path.is_file():
        return "Comic has not been generated yet.", 404

    return send_from_directory(str(OUTPUT_DIR), filename)


if __name__ == "__main__":
    print(f"Project:   {BASE_DIR}")
    print(f"Templates: {TEMPLATE_DIR}")
    print(f"Template exists: {(TEMPLATE_DIR / 'index.html').is_file()}")
    print(f"Static:    {STATIC_DIR}")
    print("Starting Katha Loka at http://127.0.0.1:5055")

    app.run(host="127.0.0.1", port=5055, debug=False)
