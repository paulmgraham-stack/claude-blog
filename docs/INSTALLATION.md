# Installation Guide

This guide covers installing `cursor-blog`, the Cursor plugin curated from
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog) (MIT)
for blog content creation, optimization, and management. The Cursor plugin is
the only supported install path.

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| [Cursor](https://cursor.com) | Latest | Runtime for the Agent Skills |
| Python | 3.11+ | Quality scoring + 5-gate delivery contract runners (analyze_blog, blog_preflight, blog_render, generate_hero, lint_prose, ...) |
| pip | Latest | Python dependency management |

Python 3.11+ is required for quality scoring and helper workflows including
`analyze_blog.py`, `blog_preflight.py`, `blog_render.py`, `generate_hero.py`,
`lint_prose.py`, and related script checks. Skills that do not invoke those
helpers still work without Python.

---

## Install the `cursor-blog` plugin

Cursor discovers skills from an installed plugin, not from a bare top-level
`skills/` directory. This repository ships the plugin under
[`../plugins/cursor-blog/`](../plugins/cursor-blog) with a
`plugins/cursor-blog/.cursor-plugin/plugin.json` manifest, and the repo-root
[`../.cursor-plugin/marketplace.json`](../.cursor-plugin/marketplace.json)
catalog lists it for GitHub import.

### Option A: Local plugin install

```bash
mkdir -p ~/.cursor/plugins/local
cp -r plugins/cursor-blog ~/.cursor/plugins/local/cursor-blog
```

Restart Cursor (or run `Developer: Reload Window`), then open Customize and
confirm "Cursor Blog" and its sub-skills appear under Skills. Local plugin
imports must be allowed in your Cursor settings (an admin controls this on
Teams and Enterprise).

### Option B: Import from GitHub

In Cursor, open Customize and choose "From GitHub Repository". The root
`.cursor-plugin/marketplace.json` lists the `cursor-blog` plugin with its
`plugins/cursor-blog` source.

---

## Install Python dependencies

The Python tooling is stdlib-first. Install the optional dependencies to unlock
readability scoring, schema detection, and media workflows:

```bash
python3 -m pip install -r requirements.txt
```

### Reproducible install via uv

For deterministic supply-chain hygiene, the repo ships `uv.lock` with SHA-256
hashes for every wheel. Reproduce the exact dev environment with:

```bash
pip install uv          # one-time
uv sync --frozen        # installs from uv.lock with hash verification
```

The `pip install -e ".[dev]"` flow also works; it resolves transitives freshly
each time. Regenerate `uv.lock` after editing `pyproject.toml` dependency
bounds:

```bash
uv lock
```

**Core dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| textstat | >=0.7.3 | Readability scoring (Flesch, Gunning Fog, SMOG) |
| beautifulsoup4 | >=4.12.0 | HTML and schema parsing |
| lxml | >=5.0.0 | XML/HTML parser backend |
| jsonschema | >=4.20.0 | JSON-LD schema validation |

**Optional dependencies** (unlock advanced features in `analyze_blog.py`):

```bash
pip install spacy                  # NER, advanced NLP
python -m spacy download en_core_web_sm
pip install sentence-transformers  # Semantic similarity / duplicate detection
pip install scikit-learn           # Topic cannibalization clustering
pip install language-tool-python   # Grammar and style checking (requires Java)
```

The analysis script works without optional dependencies by falling back to
basic mode automatically.

---

## Optional: AI image generation

`cursor-blog` can generate custom blog images via Gemini AI (hero images, inline
illustrations, social cards). This requires the nanobanana-mcp server and a free
Google AI API key.

```bash
# Get your free API key at: https://aistudio.google.com/apikey
python3 skills/blog-image/scripts/setup_image_mcp.py --key YOUR_KEY

# Verify setup
python3 skills/blog-image/scripts/validate_image_setup.py
```

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Node.js | 18+ | Runs `npx @ycse/nanobanana-mcp` |
| Google AI API key | Free tier | Image generation via Gemini |

Without this setup, all skills work normally using stock photos from
Pixabay/Unsplash/Pexels. AI image generation is an optional enhancement. Cursor
also has a native image tool.

---

## Verification

After installing the plugin, verify the tooling:

```bash
python3 scripts/analyze_blog.py --help
```

Expected output:

```
usage: analyze_blog.py [-h] [--output OUTPUT] [--batch] input

Analyze blog post quality

positional arguments:
  input                 Blog file path or directory (with --batch)

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file path (JSON)
  --batch               Analyze all blog files in directory
```

Then, inside Cursor Agent chat, describe a task in natural language (for
example "Write a blog post about home automation and score it") or type `/` and
pick a skill. The orchestrator routes to the matching sub-skill.

---

## Updating

Pull the latest changes and re-copy the plugin:

```bash
git pull
rm -rf ~/.cursor/plugins/local/cursor-blog
cp -r plugins/cursor-blog ~/.cursor/plugins/local/cursor-blog
```

Restart Cursor (or run `Developer: Reload Window`) after updating.

---

## Uninstall

Remove the local plugin copy:

```bash
rm -rf ~/.cursor/plugins/local/cursor-blog
```

If you imported the plugin from GitHub, remove it from Customize instead.

### Clean up Python dependencies (optional)

```bash
pip uninstall textstat beautifulsoup4 lxml jsonschema
```

---

## Troubleshooting installation

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skills not listed in Customize | Cursor not reloaded | Run `Developer: Reload Window` or restart Cursor |
| Local plugin import blocked | Setting disabled | Enable local plugin imports in Cursor settings (admin-controlled on Teams/Enterprise) |
| `python3: command not found` | Python not installed or not in PATH | Install Python 3.11+ via your package manager |
| `pip install` fails | Missing pip or wrong Python version | Run `python3 -m ensurepip --upgrade` |

For additional issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
