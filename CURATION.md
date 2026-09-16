# CURATION.md

## What this document is

This repository is a **curated fork** of
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog)
(MIT), prepared for **Cursor / Grok Bot house use**. Upstream is an excellent,
comprehensive Claude Code plugin suite. This fork keeps the blog and SEO skill
value and reframes the entry points so the same skills are usable from Cursor
Agent Skills, while clearly marking the parts that are Claude Code only.

Nothing here was installed into any local skills library, `~/.claude`, or a
Cursor marketplace. The only changes are to files inside this GitHub repository,
delivered through a branch and pull request.

The goal is that a reviewer can tell in one read which parts are Cursor ready and
which are left in place as upstream Claude Code reference. This file is the map.

> Attribution and license are preserved in full. See [`LICENSE`](LICENSE),
> [`NOTICE`](NOTICE), [`CITATION.cff`](CITATION.cff), and
> [`docs/CONTRIBUTORS.md`](docs/CONTRIBUTORS.md). Original author: Daniel Agrici
> (AgriciDaniel). This fork changes framing and documentation only; it does not
> claim authorship of the upstream methodology.

---

## TL;DR

| Bucket | Meaning | Where |
|---|---|---|
| Cursor ready | Works today from Cursor Agent Skills as content or Python tooling | `skills/`, `scripts/`, `tests/`, references, templates |
| Adapted | Reframed for Cursor without deleting upstream capability | SKILL.md frontmatter, `README.md` |
| Secondary (needs external setup) | Usable in Cursor only with external API keys or MCP servers | `blog-google`, `blog-audio`, `blog-notebooklm`, `blog-image` |
| Quarantined (upstream Claude Code reference) | Kept in place for upstream parity, NOT the Cursor path | install scripts, `.claude-plugin/`, `/blog` slash-command CLI framing, `agents/`, `brain/` |

Full detail and rationale follow.

---

## Kept: Cursor ready

These are the reason to use this fork. They are plain markdown skill content and
stdlib-first Python; none of them require Claude Code to be meaningful.

### Core blog and SEO skills

| Skill | Purpose | Cursor entry |
|---|---|---|
| `skills/blog/SKILL.md` | Orchestrator: routing logic, 6 pillars, scoring, delivery-contract references | Read as a skill; describe the blog task in natural language |
| `skills/blog-write` | Write new articles from scratch | "write a blog post about ..." |
| `skills/blog-rewrite` | Optimize and refresh existing posts | "rewrite / optimize this post" |
| `skills/blog-outline` | SERP-informed outlines and heading hierarchy | "outline an article on ..." |
| `skills/blog-brief` | Detailed content briefs | "brief for ..." |
| `skills/blog-seo-check` | Post-writing on-page SEO validation | "SEO check this file" |
| `skills/blog-analyze` | 5-category 100-point quality scoring | "analyze / score this post" |
| `skills/blog-strategy` | Positioning, topic clusters, ideation | "blog strategy for ..." |
| `skills/blog-geo` | GEO/AEO AI-citation readiness audit | "audit this for AI citations" |
| `skills/blog-schema` | JSON-LD schema generation | "generate schema for ..." |
| `skills/blog-repurpose` | Multi-platform repurposing | "repurpose this post" |
| `skills/blog-cannibalization` | Keyword-overlap detection | "check cannibalization" |
| `skills/blog-factcheck` | Statistic and source verification | "fact-check this post" |
| `skills/blog-persona` | Writing persona and voice profiles | "create/use a persona" |
| `skills/blog-taxonomy` | Tag and category management | "suggest taxonomy" |
| `skills/blog-calendar` | Editorial calendars | "editorial calendar" |
| `skills/blog-chart` | Inline SVG charts (internal helper) | invoked by write/rewrite |
| `skills/blog-cluster` | Semantic topic-cluster planning and execution | "plan a topic cluster" |
| `skills/blog-brand` | BRAND.md and VOICE.md context files | "set up brand context" |
| `skills/blog-discourse` | API-free last-30-days discourse research | "what are people saying about ..." |
| `skills/blog-style` | Author voice-profile learner | "learn my writing style" |
| `skills/blog-decay` | GSC content-decay detection | "find decaying content" |
| `skills/blog-flow` | FLOW framework prompts (CC BY 4.0) | "run FLOW prompts" |
| `skills/blog-multilingual` | Write plus translate plus localize plus hreflang | "publish in multiple languages" |
| `skills/blog-translate` | SEO-preserving translation | "translate this post" |
| `skills/blog-localize` | Cultural deep-adaptation per locale | "localize for DACH/FR/JA" |
| `skills/blog-locale-audit` | Multilingual content QA | "audit my translations" |

### References and templates

- `skills/blog/references/*.md` (22 reference docs): the SEO, GEO/AEO, E-E-A-T,
  schema, internal-linking, delivery-contract, editorial-heuristics, and
  research-quality knowledge. Pure guidance; fully usable in Cursor.
- `skills/blog/templates/*.md` (12 content templates): how-to, listicle, case
  study, comparison, pillar, product review, thought leadership, roundup,
  tutorial, news analysis, data research, FAQ. Pure markdown.

### Python tooling (platform-agnostic)

All of `scripts/*.py` is stdlib-first and runs anywhere Python 3.11+ runs,
independent of Claude Code:

- `analyze_blog.py`, `ai_citation_score.py` (scoring)
- `blog_preflight.py`, `blog_render.py`, `blog_hygiene.py`, `generate_hero.py`
  (delivery-contract runners and renderer)
- `cognitive_load.py`, `discourse_research.py`, `content_decay.py`,
  `style_learn.py`, `quality_gate.py` (analysis)
- `consistency_check.py`, `lint_prose.py`, `check_secrets.py`,
  `dependency_smoke.py`, `validate_public_release.py` (repo hygiene)
- `load_untrusted_root.py`, `sync_flow.py` (context loading and FLOW sync)

### Tests

- `tests/` (Python `pytest` suite) validates the tooling and skill content and
  is fully relevant to the Cursor fork. See "Tests" below.

### License, attribution, provenance

- `LICENSE`, `NOTICE`, `CITATION.cff`, `docs/CONTRIBUTORS.md`,
  `docs/ARCHITECTURE.md`, `docs/COMMANDS.md`, `docs/TEMPLATES.md` are kept.

---

## Adapted

Changes that reframe for Cursor without removing upstream capability:

1. **SKILL.md frontmatter.** `compatibility:` fields that read "Requires Claude
   Code" now read that the skills work from Cursor Agent Skills or Claude Code.
   Descriptions keep their natural-language "use when ..." triggers (already
   Cursor-friendly) and no longer imply that a `/blog` slash command is the only
   entry point. The Claude Code frontmatter fields (`user-invokable`,
   `argument-hint`) are retained so upstream parity and the upstream schema check
   still pass; Cursor ignores them harmlessly.

2. **README.md.** A curated-fork banner was added at the top so the fork is
   honest about its relationship to upstream. The install section now presents
   Cursor usage first and clearly labels the Claude Code installer flow as the
   upstream reference path. All upstream credit, links, and the installer
   integrity hashes are preserved.

---

## Secondary: usable in Cursor with external setup

These skills are not Claude Code only, but they depend on external APIs, keys, or
MCP servers. They work from Cursor once those dependencies are provided, so they
are kept, but they are not the primary Cursor value:

| Skill | External dependency |
|---|---|
| `skills/blog-google` | Google API access (PSI, CrUX, GSC, GA4, NLP, YouTube, Keyword Planner) |
| `skills/blog-audio` | Gemini TTS API key |
| `skills/blog-notebooklm` | NotebookLM via browser automation (Patchright/Playwright) |
| `skills/blog-image` | Gemini image generation (Cursor also has a native image tool) |

Their `scripts/requirements.lock` files and hash-locked dependency smoke tests
are kept unchanged.

---

## Quarantined: upstream Claude Code reference

These artifacts are Claude Code specific. They are **kept in place** so the fork
stays a faithful, low-drift mirror of upstream and so the upstream test suite
keeps passing, but they are **not** the Cursor path. See
[`docs/upstream-claude-code/README.md`](docs/upstream-claude-code/README.md) for
the in-tree index.

| Artifact | Why it is Claude Code specific | Cursor equivalent |
|---|---|---|
| `install.sh`, `install.ps1` | Copy skills into `~/.claude/skills`, agents into `~/.claude/agents`, scripts into `~/.claude/scripts` | Not needed: read `skills/**/SKILL.md` in place |
| `uninstall.sh`, `uninstall.ps1` | Remove the `~/.claude` install | Not needed |
| `.claude-plugin/plugin.json` | Claude Code plugin manifest | No manifest needed for Cursor Agent Skills |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog | Not applicable |
| `/blog <command>` slash CLI framing | Claude Code slash commands and `argument-hint` | In Cursor, invoke skills by natural language; the routing table is still useful as a capability map |
| `agents/*.md` | Claude Code subagent format (`tools:` frontmatter, Task dispatch) | Cursor has its own subagent/Task model; these read fine as role specifications and are kept as reference |
| `brain/` | Vendored Obsidian authoring brain; upstream content-provenance tool, never part of the plugin payload | Not used by the Cursor skill surface |
| `claude plugin validate .` (CI job `validate-skills`) | Requires the Claude Code CLI | See "Tests" for what runs without it |

Nothing in this bucket was deleted, so reverting the fork's framing to a pure
upstream mirror is trivial.

---

## How to use the curated set in Cursor

Cursor Agent Skills are discovered from `SKILL.md` files and read on demand;
there is no install step and no `/blog` CLI requirement.

1. **Point Cursor at the skills.** Add this repo (or the `skills/` directory) to
   a Cursor workspace, or reference the skills from your Cursor rules/skills
   configuration. Each `skills/*/SKILL.md` carries a `description` with
   natural-language triggers that Cursor uses to decide when a skill applies.

2. **Invoke by intent, not by slash command.** Instead of `/blog write <topic>`,
   ask in natural language, for example "Write a blog post about X and score it".
   The orchestrator routing table in `skills/blog/SKILL.md` still documents the
   capability map, and the sub-skill `description` fields still fire on the same
   trigger phrases.

3. **Run the Python tooling directly.** The delivery-contract and scoring scripts
   are plain CLIs:

   ```bash
   python3 scripts/analyze_blog.py <file-or-dir>
   python3 scripts/ai_citation_score.py <file>
   python3 scripts/blog_render.py --md <post>.md --out-dir <folder>
   python3 scripts/blog_preflight.py --draft <folder> --strict
   ```

4. **Optional context files.** `BRAND.md`, `VOICE.md`, and `DISCOURSE.md` at a
   project root are loaded through `scripts/load_untrusted_root.py`, which fences
   untrusted content with a CSPRNG nonce. This works from Cursor as well.

5. **Secondary skills** (`blog-google`, `blog-audio`, `blog-notebooklm`,
   `blog-image`) need their external keys or MCP servers before they do anything
   useful. Provide those through Cursor secrets or MCP configuration.

---

## Tests: what still applies after curation

The Python `pytest` suite is platform-agnostic and remains the relevant quality
gate for this fork. With the runtime dependencies installed it passes:

```bash
pip install textstat beautifulsoup4 pillow markdown lxml jsonschema google-api-python-client
python3 -m pytest tests/
python3 scripts/lint_prose.py
python3 scripts/consistency_check.py --root .
python3 scripts/check_secrets.py
```

Observed result on this fork: the full `tests/` suite passes (347 passed,
1 skipped at the time of curation). The skip and any environment-specific
behavior come from optional heavy dependencies, not from the curation.

### Checks that DO apply (kept green)

- `tests/` full suite: scoring, delivery contract, security guardrails,
  installer-sync, command coherence, version coherence, release safeguards,
  prose lint, and the untrusted-root loader.
- `scripts/lint_prose.py` (no em dash, en dash, or spaced double-hyphen in prose).
- `scripts/consistency_check.py` (reference targets and FLOW locks).
- `scripts/check_secrets.py` (secret adjudication).

Note: several of these upstream tests assert Claude Code specific facts (for
example that `install.sh` references the ledger path, that `README.md` contains
the installer hashes, and that the `/blog` command sets in `SKILL.md` and
`docs/COMMANDS.md` match). Because the fork keeps those artifacts in place
rather than deleting them, those tests continue to pass. This is intentional:
low drift keeps the upstream suite meaningful.

### Checks that do NOT apply in Cursor (Claude Code only)

- `claude plugin validate .` and the CI `validate-skills` job that installs the
  Claude Code CLI. This validates the Claude Code plugin packaging, which is not
  how Cursor consumes skills. It is left unmodified as upstream reference and is
  not required for the Cursor use case. If run without the Claude Code CLI it
  simply cannot execute; that is expected and documented here rather than forced.

---

## What was NOT done (by design)

- No files were deleted or moved out of the repository.
- No `~/.claude`, local skills library, or Cursor marketplace was touched.
- No license, copyright, `NOTICE`, or attribution text was removed or weakened.
- No URLs, metrics, versions, or installer hashes were invented or altered.
- The upstream version string (`2.2.0`) is left unchanged across all coherence
  surfaces.
