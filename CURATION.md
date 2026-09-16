# CURATION.md

## What this document is

This repository is a **curated fork** of
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog)
(MIT), prepared for **Cursor / Grok Bot house use**. Upstream is an excellent,
comprehensive Claude Code plugin suite. This fork packages the blog and SEO
skills as a real **Cursor plugin** named `cursor-blog` (display name
"Cursor Blog") under [`plugins/cursor-blog/`](plugins/cursor-blog). The
Claude Code only leftovers have been removed so the repository reads as a
Cursor plugin repo, not a dual Claude/Cursor mirror.

Nothing here was installed onto anyone's machine, into `~/.claude`, into
`~/.cursor`, or into Grok Bot house skills. The only changes are to files inside
this GitHub repository, delivered through a branch and pull request.

The goal is that a reviewer can tell in one read what is Cursor ready and what
was adapted from upstream. This file is the map.

> Attribution and license are preserved in full. See [`LICENSE`](LICENSE),
> [`NOTICE`](NOTICE), [`CITATION.cff`](CITATION.cff), and
> [`docs/CONTRIBUTORS.md`](docs/CONTRIBUTORS.md), and the copies bundled in the
> plugin at [`plugins/cursor-blog/LICENSE`](plugins/cursor-blog/LICENSE) and
> [`plugins/cursor-blog/NOTICE`](plugins/cursor-blog/NOTICE). Original author:
> Daniel Agrici (AgriciDaniel). This fork repackages and reframes upstream for
> Cursor; it does not claim authorship of the upstream methodology.

---

## TL;DR

| Bucket | Meaning | Where |
|---|---|---|
| The plugin | The Cursor plugin `cursor-blog`: a self-contained, discoverable copy of the skills, references, templates, and Python tooling | `plugins/cursor-blog/`, `.cursor-plugin/marketplace.json` |
| Source tree | The skills and tooling, kept in place so the test suite stays green and the plugin can be regenerated | `skills/`, `scripts/`, `tests/` |
| Secondary (needs external setup) | Bundled in the plugin but only work with external API keys or MCP servers | `blog-google`, `blog-audio`, `blog-notebooklm`, `blog-image` |
| Removed (Claude Code only) | Deleted from this repository during Cursor cleanup | install/uninstall scripts, `.claude-plugin/`, subagent files (`agents/`), the vendored Brain (`brain/`), and `CLAUDE.md` |

Full detail and rationale follow.

---

## The `cursor-blog` Cursor plugin

Cursor does **not** auto-scan a repository's bare top-level `skills/` directory
just because the repo is open. Cursor discovers skills from supported roots
(`.cursor/skills/`, `.agents/skills/`, and the Claude/Codex compatibility roots)
or from an installed **plugin**. Per the Cursor docs, skills are not imported on
their own; to bring skills in from a GitHub repository you package them in a
plugin and install it (see
[Skill directories](https://cursor.com/docs/skills.md#skill-directories),
[Installing skills from a repository](https://cursor.com/docs/skills.md#installing-skills-from-a-repository),
and [Plugins](https://cursor.com/docs/plugins)). The earlier version of this fork
wrongly implied a bare `skills/` scan would work; that has been replaced with a
real plugin.

### Layout

This fork follows the Cursor multi-plugin
[plugin template](https://github.com/cursor/plugin-template):

```text
.cursor-plugin/
  marketplace.json                     # marketplace catalog listing the plugin
plugins/
  cursor-blog/
    .cursor-plugin/plugin.json         # Cursor Plugin manifest (name: cursor-blog)
    README.md                          # plugin-level readme + local install
    LICENSE, NOTICE                    # MIT license + attribution, bundled
    assets/logo.svg
    skills/<name>/SKILL.md             # the discoverable Agent Skills
    scripts/*.py                       # scoring, rendering, delivery-contract CLIs
```

- `plugins/cursor-blog/.cursor-plugin/plugin.json` is a **Cursor Plugin**
  manifest: `name` is the kebab-case `cursor-blog`, with `displayName`,
  `description`, `version`, `license` (MIT), `author` (AgriciDaniel), and an
  explicit `"skills": "./skills/"` path so discovery matches shipping Cursor
  skill-plugins (`cursor-team-kit`, `superpowers`, and gsap all declare a
  `skills` path).
- The repo-root `.cursor-plugin/marketplace.json` catalog lists the plugin with
  `source: ./plugins/cursor-blog`, so Cursor can import the repo with Customize ->
  "From GitHub Repository".

### Verify discoverability (one-time, local to Cursor)

This step cannot be run from a cloud VM or from CI; it needs a Cursor client.
After installing the plugin (see below), open Customize -> Skills and confirm
"Cursor Blog" and its sub-skills are listed under "Agent Decides". You can also
type `/` in Agent chat and confirm the skills appear. If they do not, check that
local plugin imports are allowed in your Cursor settings. The manifest and layout
already pass the Cursor `plugin-template` validator
(`scripts/validate-template.mjs`), but only a real Cursor load proves live
discoverability.

### Why the plugin is a copy, not the top-level `skills/`

A Cursor plugin must be a self-contained directory that Cursor discovers. To make
`cursor-blog` genuinely discoverable (not an orphan folder Cursor ignores) while
keeping this fork a low-drift mirror of upstream, the plugin bundles a copy of the
skills, references, templates, and scripts under `plugins/cursor-blog/`. The
original `skills/` and `scripts/` trees stay at the repo root as the source of
truth and as what the upstream `tests/` suite exercises. Regenerate the plugin
payload from the source tree with:

```bash
rm -rf plugins/cursor-blog/skills plugins/cursor-blog/scripts
cp -r skills plugins/cursor-blog/skills
cp -r scripts plugins/cursor-blog/scripts
```

Installing this plugin is a normal Cursor plugin install; it is not a house/global
skills-library install and was not performed as part of this curation.

---

## What the plugin includes

All 32 skill directories are bundled so the orchestrator's routing table stays
coherent. They fall into two usability tiers.

### Core blog and SEO skills (ready)

The orchestrator `blog` plus the sub-skills below are plain markdown skill content
and stdlib-first Python; none require Claude Code to be meaningful. Invoke by
intent in natural language, or with `/` in Cursor Agent chat.

| Skill | Purpose |
|---|---|
| `blog` | Orchestrator: routing, 6 pillars, scoring, delivery-contract references |
| `blog-write` | Write new articles from scratch |
| `blog-rewrite` | Optimize and refresh existing posts |
| `blog-outline` | SERP-informed outlines and heading hierarchy |
| `blog-brief` | Detailed content briefs |
| `blog-seo-check` | Post-writing on-page SEO validation |
| `blog-analyze` | 5-category 100-point quality scoring |
| `blog-strategy` | Positioning, topic clusters, ideation |
| `blog-geo` | GEO/AEO AI-citation readiness audit |
| `blog-schema` | JSON-LD schema generation |
| `blog-repurpose` | Multi-platform repurposing |
| `blog-cannibalization` | Keyword-overlap detection |
| `blog-factcheck` | Statistic and source verification |
| `blog-persona` | Writing persona and voice profiles |
| `blog-taxonomy` | Tag and category management |
| `blog-calendar` | Editorial calendars |
| `blog-chart` | Inline SVG charts (internal helper) |
| `blog-cluster` | Semantic topic-cluster planning and execution |
| `blog-brand` | BRAND.md and VOICE.md context files |
| `blog-discourse` | API-free last-30-days discourse research |
| `blog-style` | Author voice-profile learner |
| `blog-decay` | GSC content-decay detection |
| `blog-flow` | FLOW framework prompts (CC BY 4.0) |
| `blog-multilingual` | Write plus translate plus localize plus hreflang |
| `blog-translate` | SEO-preserving translation |
| `blog-localize` | Cultural deep-adaptation per locale |
| `blog-locale-audit` | Multilingual content QA |

References (`skills/blog/references/*.md`, 22 docs) and templates
(`skills/blog/templates/*.md`, 12 docs) travel with the `blog` skill and are pure
markdown, fully usable in Cursor. The Python tooling in `scripts/*.py` is
stdlib-first (scoring, rendering, delivery-contract runners, analysis, and repo
hygiene).

### Secondary skills (need external setup)

Bundled for completeness and to keep routing coherent, but they only work once you
provide the relevant keys or MCP servers:

| Skill | External dependency |
|---|---|
| `blog-google` | Google API access (PSI, CrUX, GSC, GA4, NLP, YouTube, Keyword Planner) |
| `blog-audio` | Gemini TTS API key |
| `blog-notebooklm` | NotebookLM via browser automation (Patchright/Playwright) |
| `blog-image` | Gemini image generation (Cursor also has a native image tool) |

---

## Orchestrated capability vs guidance and CLIs

Be precise about what "ready" means for `blog-write` and `blog-rewrite`:

- **Ready as guidance and direct CLIs.** The skill instructions and the Python
  CLIs (`scripts/analyze_blog.py`, `scripts/ai_citation_score.py`,
  `scripts/blog_render.py`, `scripts/blog_preflight.py`,
  `scripts/generate_hero.py`) run in Cursor with no Claude Code dependency.
- **Fully orchestrated 5-gate delivery contract needs adaptation.** Upstream
  `blog-write` / `blog-rewrite` dispatch Task subagents (`blog-researcher`,
  `blog-writer`, `blog-seo`, and a blocking `blog-reviewer`) and resolve helper
  scripts from `$HOME/.claude/scripts`. Those subagent files were removed in the
  Cursor cleanup, and there is no `~/.claude` install in Cursor; the roles run
  inline instead.

The orchestrator carries a "Running in Cursor" section
(`skills/blog/SKILL.md`, copied into the plugin) that documents the two
adaptations that make the contract run in Cursor:

1. **Point the absolute helper overrides at the plugin's own scripts** (the
   security model already allows an operator-pinned absolute path, and forbids the
   untrusted current working directory):

   ```bash
   export CLAUDE_BLOG_SCRIPTS_DIR="/abs/path/to/cursor-blog/scripts"
   export CLAUDE_BLOG_LOAD_UNTRUSTED_HELPER="/abs/path/to/cursor-blog/scripts/load_untrusted_root.py"
   ```

2. **Run the agent roles inline using bundled skills**, since the plugin does not
   ship the Claude Code subagents. Where the suite mentions `blog-researcher`,
   `blog-writer`, `blog-seo`, or `blog-reviewer`, the main agent performs those
   roles inline from content that is in the payload: `blog-write` (research and
   drafting), `blog-seo-check` (on-page validation), and `blog-analyze` scored
   against `skills/blog/references/quality-scoring.md` and
   `skills/blog/references/editorial-heuristics.md` (the Gate 4 review). The
   Python delivery-contract CLIs run directly.

So `blog-write` end-to-end is not a zero-config button in Cursor; it is ready as
guidance plus CLIs, and fully orchestrated with the setup above.

---

## Adapted

Changes that reframe and wire the fork for Cursor without removing upstream
capability:

1. **Packaged as the `cursor-blog` Cursor plugin.** New
   `plugins/cursor-blog/.cursor-plugin/plugin.json` (with an explicit
   `"skills": "./skills/"` path, matching shipping Cursor skill-plugins such as
   `cursor-team-kit` and `superpowers`) and `.cursor-plugin/marketplace.json`,
   with the skills/references/templates/scripts copied into the plugin payload so
   Cursor discovers them.
2. **SKILL.md frontmatter.** `compatibility:` fields that read "Requires Claude
   Code" now say the skills work from Cursor Agent Skills or Claude Code. The
   orchestrator `description` no longer implies `/blog` is the only entry point.
   The Claude Code frontmatter fields (`user-invokable`, `argument-hint`) are
   retained so upstream parity and the upstream schema check still pass; Cursor
   ignores them harmlessly.
3. **Orchestrator "Running in Cursor" section** documenting the helper overrides
   and inline-agent fallback (see above).
4. **README.md and docs/INSTALLATION.md.** The README banner and a "Use in
   Cursor: the `cursor-blog` plugin" section describe the Cursor plugin as the
   only install path; `docs/INSTALLATION.md` is a Cursor plugin install guide.
   Upstream credit and links are preserved.

---

## Removed: Claude Code only leftovers

These artifacts were Claude Code specific and have been **deleted** from this
repository so it reads cleanly as a Cursor plugin repo rather than a dual
Claude/Cursor mirror. Full upstream copies remain available at
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog).

| Removed artifact | Why it was Claude Code specific | In Cursor |
|---|---|---|
| `install.sh`, `install.ps1` | Copied skills, agents, and scripts into `~/.claude` | Not needed: install the `cursor-blog` plugin instead |
| `uninstall.sh`, `uninstall.ps1` | Removed the `~/.claude` install | Not needed |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest | Replaced by `plugins/cursor-blog/.cursor-plugin/plugin.json` |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog | Replaced by `.cursor-plugin/marketplace.json` |
| `agents/*.md` | Claude Code subagent format (`tools:` frontmatter, Task dispatch) | Run the roles inline or register Cursor subagents |
| `brain/` | Vendored Obsidian authoring brain; never part of any plugin payload | Not used by the Cursor skill surface |
| `CLAUDE.md` | Claude Code project instructions | Not used by Cursor |
| `docs/upstream-claude-code/` | Index of the quarantined Claude Code artifacts | No longer needed once the artifacts are removed |

---

## How to install and use in Cursor

1. **Install the plugin locally** (no marketplace required):

   ```bash
   mkdir -p ~/.cursor/plugins/local
   cp -r plugins/cursor-blog ~/.cursor/plugins/local/cursor-blog
   ```

   Restart Cursor or run `Developer: Reload Window`, then open Customize and
   confirm "Cursor Blog" appears under Skills. Local plugin imports must be
   allowed in your Cursor settings (an admin controls this on Teams and
   Enterprise). Alternatively, import the repository from GitHub in Customize with
   "From GitHub Repository"; the root `.cursor-plugin/marketplace.json` lists the
   plugin. Marketplace publish is optional and can be done later.

2. **Invoke by intent.** Ask in natural language, for example "Write a blog post
   about X and score it", or type `/` and pick a skill.

3. **Run the Python tooling directly** (bundled under the plugin's `scripts/`):

   ```bash
   python3 scripts/analyze_blog.py <file-or-dir>
   python3 scripts/ai_citation_score.py <file>
   python3 scripts/blog_render.py --md <post>.md --out-dir <folder>
   python3 scripts/blog_preflight.py --draft <folder> --strict
   ```

4. **For the full delivery contract**, set the helper overrides and use the
   inline-agent fallback described in "Orchestrated capability vs guidance and
   CLIs".

5. **Secondary skills** need their external keys or MCP servers first.

---

## Tests: reproduction and what applies

The Python `pytest` suite is platform-agnostic and remains the relevant quality
gate. The `pytest` and `detect-secrets` tools plus the runtime dependencies come
from the project's `dev` extras, which is exactly what the repository CI installs
(`pip install -e ".[dev]"`). Reproduce in a clean checkout:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python3 -m pytest tests/
python3 scripts/lint_prose.py
python3 scripts/consistency_check.py --root .
python3 scripts/check_secrets.py
```

### Checks that apply (kept green)

- `tests/` full suite: scoring, delivery contract, security guardrails,
  command coherence, version coherence, release safeguards, prose lint, and the
  untrusted-root loader.
- `scripts/lint_prose.py` (no em dash, en dash, or spaced double-hyphen in prose).
- `scripts/consistency_check.py --root .` (reference targets and FLOW locks; it
  scans `docs/`, `skills/`, `.github/`, so the plugin copy under `plugins/` does
  not affect it).
- `scripts/check_secrets.py` (secret adjudication).

Tests that only asserted Claude Code installer or plugin facts (installer-sync,
installer hashes, the Claude plugin manifest, the public-release validator, and
the Brain gate) were removed along with the artifacts they covered, so the suite
stays green without dead Claude Code coverage.

---

## What was NOT done (by design)

- No plugin was installed onto any machine, into `~/.claude`, `~/.cursor`, or Grok
  Bot house skills.
- No license, copyright, `NOTICE`, or attribution text was removed or weakened;
  the plugin bundles its own `LICENSE` and `NOTICE`.
- No URLs, metrics, or versions were invented or altered.
- The upstream version string (`2.2.0`) is left unchanged across all coherence
  surfaces, and reused for the plugin manifest.
