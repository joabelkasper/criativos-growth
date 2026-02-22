# CLAUDE.md

This file provides guidance for AI assistants (Claude and others) working in this repository.

## Project Overview

**criativos-growth** — a web application for batch-generating ad creatives (copy + images) for paid traffic campaigns across Meta, Google Ads, and TikTok.

- **Language**: Python 3.11+
- **Framework**: FastAPI with Jinja2 templates
- **AI**: Anthropic Claude API (copy generation)
- **Image processing**: Pillow (image composition)

## Repository Structure

```
criativos-growth/
├── app/
│   ├── main.py                     # FastAPI app entry point
│   ├── api/routes/
│   │   └── creatives.py            # Web routes (form, generation, image serving)
│   ├── core/
│   │   ├── config.py               # Settings (env vars via pydantic-settings)
│   │   └── platforms.py            # Platform format specs (Meta, Google, TikTok)
│   ├── models/
│   │   └── schemas.py              # Pydantic models (CampaignBrief, CopyVariation, etc.)
│   ├── services/
│   │   ├── copy_generator.py       # Claude API integration for ad copy
│   │   ├── image_composer.py       # Pillow-based image composition
│   │   └── creative_engine.py      # Orchestrates copy generation + image composition
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html              # Campaign brief form
│   │   └── results.html            # Generated creatives display
│   └── static/css/
│       └── style.css               # Dark-themed UI styles
├── assets/templates/               # (future) image templates and backgrounds
├── output/                         # Generated creative files (gitignored)
├── requirements.txt
├── .env.example
├── .gitignore
├── CLAUDE.md
└── README.md
```

## Development Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your Anthropic API key

# 3. Run the dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app will be available at `http://localhost:8000`.

## Available Commands

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Start dev server with hot reload |
| `pip install -r requirements.txt` | Install/update dependencies |

## Environment Variables

Defined in `.env` (see `.env.example` for template):

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | API key for Claude (copy generation) |
| `OUTPUT_DIR` | No | Directory for generated files (default: `output`) |

## Architecture

### Request Flow

1. User fills campaign brief form at `/`
2. `POST /generate` receives the brief
3. **Copy Generator** (`copy_generator.py`) calls Claude API to generate N copy variations (hook, headline, body, CTA)
4. **Image Composer** (`image_composer.py`) creates PNG images for each copy × platform format combination using Pillow
5. **Creative Engine** (`creative_engine.py`) orchestrates steps 3–4 and returns all results
6. Results page displays all creatives grouped by copy variation

### Platform Formats

Defined in `app/core/platforms.py`:

- **Meta**: Feed 1080×1080, Feed 1080×1350, Stories/Reels 1080×1920
- **Google Ads**: Leaderboard 728×90, Medium Rectangle 300×250, Large Rectangle 336×280, Skyscraper 160×600
- **TikTok**: Feed 1080×1920

### Key Models (in `app/models/schemas.py`)

- `CampaignBrief` — input from the user (product info, audience, tone, colors, platforms)
- `CopyVariation` — a single copy variant (hook, headline, body, cta)
- `GeneratedCreative` — one creative asset (copy + format + image path)
- `GenerationResult` — full output of a generation run

## Code Conventions

- **Python style**: Standard Python conventions, type hints throughout
- **Naming**: `snake_case` for files and functions, `PascalCase` for classes
- **Field naming**: Avoid Pydantic reserved names (use `ad_copy` not `copy` in models)
- **Imports**: Group by stdlib → third-party → local, alphabetically within groups
- **Templates**: Jinja2 with `{% block %}` inheritance from `base.html`
- **Generated files**: Written to `output/<campaign_id>/` — never committed to git

## Git Workflow

### Branches

- `master` — main/stable branch
- Feature and AI-assisted work branches use the pattern `claude/<descriptor>-<session-id>`

### Commit Conventions

Use clear, descriptive commit messages in imperative form:

```
Add copy generation service using Claude API
Fix image text wrapping for narrow formats
Update platform specs for TikTok
```

### Push Instructions

Always push with upstream tracking:

```bash
git push -u origin <branch-name>
```

Branch names for AI-assisted work must start with `claude/` and end with the session ID.

## Testing

> No testing framework is configured yet. When added, document the test runner, file locations, and commands here.

## For AI Assistants

- Read existing service files before modifying — understand the current copy generation prompt and image composition logic
- The Claude model used for copy generation is configured in `app/core/config.py` (`settings.model`)
- Platform format specs live in `app/core/platforms.py` — add new platforms there
- Generated output goes to `output/` and is served via `/creative/{campaign_id}/{filename}`
- Commit and push changes to the designated `claude/` branch — never push to `master` without explicit permission
- When adding new dependencies, update `requirements.txt`
- When adding new environment variables, update both `.env.example` and this file
