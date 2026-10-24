
#!/usr/bin/env bash
set -euo pipefail

PROJECT="katha-loka"

echo "Creating Katha Loka project structure..."

mkdir -p "$PROJECT"/{app/{routes,services,templates,static/{css,js,images/{characters,backgrounds,generated}}},engine/{characters,layouts,renderers,story_parser},stories/{drafts,published},output/{comics,previews},config,tests,docs,scripts}

cd "$PROJECT"

# Create starter files
touch \
  app/__init__.py \
  app/routes/__init__.py \
  app/routes/comics.py \
  app/services/__init__.py \
  app/services/comic_service.py \
  app/templates/index.html \
  app/templates/reader.html \
  app/static/css/style.css \
  app/static/js/app.js \
  engine/__init__.py \
  engine/characters/__init__.py \
  engine/characters/library.py \
  engine/layouts/__init__.py \
  engine/layouts/vertical.py \
  engine/renderers/__init__.py \
  engine/renderers/pillow_renderer.py \
  engine/story_parser/__init__.py \
  engine/story_parser/parser.py \
  config/settings.py \
  tests/__init__.py \
  tests/test_comic_engine.py \
  scripts/run.sh \
  requirements.txt \
  .gitignore \
  README.md

cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.py[cod]
.env
output/comics/*
output/previews/*
!output/comics/.gitkeep
!output/previews/.gitkeep
EOF

touch output/comics/.gitkeep output/previews/.gitkeep

cat > requirements.txt <<'EOF'
Flask
Pillow
EOF

cat > README.md <<'EOF'
# Katha Loka Comic Studio

A lightweight, local-first bilingual comic generation project.

## Initial stack
- Python
- Flask
- Pillow
- HTML, CSS and JavaScript
- Kannada and English stories

## Planned features
- Reusable cartoon characters
- Vertical-scrolling comic panels
- Speech bubbles and narration
- Story editor and preview
- Bilingual reading experience
EOF

cat > scripts/run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate
python app.py
EOF

chmod +x scripts/run.sh

echo
echo "Project structure created successfully."
echo "Location: $(pwd)"
echo
find . -maxdepth 4 -type d | sort
echo
echo "Next: cd $PROJECT"
