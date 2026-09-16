# CURATION.md

## What this document is

This repository is a **curated fork** of
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog)
(MIT), prepared for **Cursor / Grok Bot house use**. Upstream is an excellent,
comprehensive Claude Code plugin suite. This fork packages the Cursor-ready blog
and SEO skills as a real **Cursor plugin** named `cursor-blog` (display name
"Cursor Blog") under [`plugins/cursor-blog/`](plugins/cursor-blog), and clearly
marks the parts that are Claude Code only.

Nothing here was installed onto anyone's machine, into `~/.claude`, into
`~/.cursor`, or into Grok Bot house skills. The only changes are to files inside
this GitHub repository, delivered through a branch and pull request.

The goal is that a reviewer can tell in one read which parts are Cursor ready and
which are left in place as upstream Claude Code reference. This file is the map.

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
| The plugin | The Cursor plugin `cursor-blog`: a self-contained, discoverable copy of the Cursor-ready skills, references, templates, and Python tooling | `plugins/cursor-blog/`, `.cursor-plugin/marketplace.json` |
| Upstream source tree | The original skills and tooling, kept in place so the upstream test suite stays green and the plugin can be regenerated | `skills/`, `scripts/`, `tests/` |
| Secondary (needs external setup) | Bundled in the plugin but only work with external API keys or MCP servers | `blog-google`, `blog-audio`, `blog-notebooklm`, `blog-image` |
| Quarantined (upstream Claude Code reference) | Kept in the repo root, NOT part of the plugin payload | install scripts, `.claude-plugin/`, `/blog` slash-command CLI framing, `agents/`, `brain/` |

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
  `description`, `version`, `license` (MIT), and `author` (AgriciDaniel).
- The repo-root `.cursor-plugin/marketplace.json` catalog lists the plugin with
  `source: ./plugins/cursor-blog`, so Cursor can import the repo with Customize ->
  "From GitHub Repository".

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
  scripts from `$HOME/.claude/scripts`. Those subagents live in `agents/`, which
  is **not** part of the plugin, and there is no `~/.claude` install in Cursor.

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

2. **Run the agent roles inline** from `agents/*.md`, or register equivalent
   Cursor subagents, since the plugin does not bundle the Claude Code subagents.
   The Python delivery-contract CLIs run directly either way, and the Gate 4
   review is scored against `skills/blog/references/quality-scoring.md`.

So `blog-write` end-to-end is not a zero-config button in Cursor; it is ready as
guidance plus CLIs, and fully orchestrated with the setup above.

---

## Adapted

Changes that reframe and wire the fork for Cursor without removing upstream
capability:

1. **Packaged as the `cursor-blog` Cursor plugin.** New
   `plugins/cursor-blog/.cursor-plugin/plugin.json` and
   `.cursor-plugin/marketplace.json`, with the skills/references/templates/scripts
   copied into the plugin payload so Cursor discovers them.
2. **SKILL.md frontmatter.** `compatibility:` fields that read "Requires Claude
   Code" now say the skills work from Cursor Agent Skills or Claude Code. The
   orchestrator `description` no longer implies `/blog` is the only entry point.
   The Claude Code frontmatter fields (`user-invokable`, `argument-hint`) are
   retained so upstream parity and the upstream schema check still pass; Cursor
   ignores them harmlessly.
3. **Orchestrator "Running in Cursor" section** documenting the helper overrides
   and inline-agent fallback (see above).
4. **README.md and docs/INSTALLATION.md.** A curated-fork banner and a "Use in
   Cursor: the `cursor-blog` plugin" section were added; `docs/INSTALLATION.md`
   now carries an upstream-reference-only banner so the Claude Code installer
   guide cannot be mistaken for the Cursor path. Upstream credit, links, and the
   installer integrity hashes are preserved.

---

## Quarantined: upstream Claude Code reference (not in the plugin payload)

These artifacts are Claude Code specific. They are **kept in the repo root** so
the fork stays a faithful, low-drift mirror of upstream and the upstream test
suite keeps passing, but they are **excluded from `plugins/cursor-blog/`**. See
[`docs/upstream-claude-code/README.md`](docs/upstream-claude-code/README.md) for
the in-tree index.

| Artifact | Why it is Claude Code specific | In Cursor |
|---|---|---|
| `install.sh`, `install.ps1` | Copy skills, agents, and scripts into `~/.claude` | Not needed: install the `cursor-blog` plugin instead |
| `uninstall.sh`, `uninstall.ps1` | Remove the `~/.claude` install | Not needed |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest | Replaced by `plugins/cursor-blog/.cursor-plugin/plugin.json` |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog | Replaced by `.cursor-plugin/marketplace.json` |
| `/blog <command>` slash CLI framing | Claude Code slash commands and `argument-hint` | Invoke skills by natural language or `/skill-name`; the routing table is still a capability map |
| `agents/*.md` | Claude Code subagent format (`tools:` frontmatter, Task dispatch) | Not bundled; run their instructions inline or register Cursor subagents |
| `brain/` | Vendored Obsidian authoring brain; never part of any plugin payload | Not used by the Cursor skill surface |
| `claude plugin validate .` (CI job `validate-skills`) | Requires the Claude Code CLI | See "Tests" for what runs without it |

Nothing in this bucket was deleted, so reverting the fork to a pure upstream
mirror is trivial.

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

Honesty about corroboration: `347 passed, 1 skipped` is an author-local
observation. GitHub Actions appears disabled on this fork (no CI runs are
reported on the repository), so this PR currently has no independent CI check. The
repository already contains `.github/workflows/ci.yml`, which runs the full
`pytest` suite via `pip install -e ".[dev]"` on `pull_request` to `main`; enabling
Actions on the fork will corroborate the result automatically. Independent of
CI, `scripts/lint_prose.py` and `scripts/consistency_check.py --root .` pass
(0 errors, 0 warnings).

### Checks that DO apply (kept green)

- `tests/` full suite: scoring, delivery contract, security guardrails,
  installer-sync, command coherence, version coherence, release safeguards,
  prose lint, and the untrusted-root loader.
- `scripts/lint_prose.py` (no em dash, en dash, or spaced double-hyphen in prose).
- `scripts/consistency_check.py --root .` (reference targets and FLOW locks; it
  scans `docs/`, `skills/`, `agents/`, `.github/`, so the plugin copy under
  `plugins/` does not affect it).
- `scripts/check_secrets.py` (secret adjudication).

Note: several upstream tests assert Claude Code specific facts (for example that
`install.sh` references the ledger path, that `README.md` contains the installer
hashes, and that the `/blog` command sets in `SKILL.md` and `docs/COMMANDS.md`
match). Because the fork keeps those artifacts in place rather than deleting them,
those tests continue to pass. This is intentional: low drift keeps the upstream
suite meaningful.

### Checks that do NOT apply in Cursor (Claude Code only)

- `claude plugin validate .` and the CI `validate-skills` job that installs the
  Claude Code CLI. This validates the Claude Code plugin packaging, which is not
  how Cursor consumes the plugin. It is left unmodified as upstream reference and
  is not required for the Cursor use case. If run without the Claude Code CLI it
  simply cannot execute; that is documented here rather than forced.

---

## What was NOT done (by design)

- No files were deleted or moved out of the upstream source tree; the plugin is an
  additive copy.
- No plugin was installed onto any machine, into `~/.claude`, `~/.cursor`, or Grok
  Bot house skills.
- No license, copyright, `NOTICE`, or attribution text was removed or weakened;
  the plugin bundles its own `LICENSE` and `NOTICE`.
- No URLs, metrics, versions, or installer hashes were invented or altered.
- The upstream version string (`2.2.0`) is left unchanged across all coherence
  surfaces, and reused for the plugin manifest.
- The GitHub repository was not renamed; only the plugin identity is `cursor-blog`.
