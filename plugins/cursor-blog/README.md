# Cursor Blog (`cursor-blog`)

A Cursor plugin of blog and SEO **Agent Skills**, adapted from
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog) (MIT).
It packages the Cursor-ready blog workflow (write, rewrite, outline, SEO check,
analyze, strategy, GEO/AEO, schema, repurpose, fact-check, persona, topic
clusters, and multilingual publishing) as discoverable Cursor skills.

> Attribution: the skill content, references, templates, and scripts are the work
> of Daniel Agrici (AgriciDaniel) and contributors, under the MIT License. See
> [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE) in this plugin folder. This plugin
> repackages that work for Cursor; it does not claim upstream authorship.

## What is in this plugin

| Component | Location |
|---|---|
| Skills | `skills/<name>/SKILL.md` (orchestrator `blog` plus sub-skills) |
| References and templates | `skills/blog/references/*.md`, `skills/blog/templates/*.md` |
| Python tooling | `scripts/*.py` (scoring, rendering, delivery-contract runners) |
| Manifest | `.cursor-plugin/plugin.json` |

The orchestrator skill (`skills/blog/SKILL.md`) has a "Running in Cursor" section
that explains how the delivery contract runs without Claude Code subagents or a
`~/.claude` install.

### Skills that need external setup (secondary)

These are included for completeness but only work once you provide the relevant
API keys or MCP servers; they are not required for the core writing workflow:

- `blog-google` (Google APIs: PSI, CrUX, GSC, GA4, NLP, YouTube, Keyword Planner)
- `blog-audio` (Gemini TTS)
- `blog-notebooklm` (NotebookLM via browser automation)
- `blog-image` (Gemini image generation; Cursor also has a native image tool)

### Not part of this plugin

The upstream Claude Code installers, the Claude plugin manifest, the Claude Code
subagent files, and the vendored Brain are not part of this plugin. Those
Claude Code only leftovers have been removed from the repository; full upstream
copies remain at
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog). See
the repository [`CURATION.md`](../../CURATION.md).

## Install locally in Cursor

You do not need this to be published to a marketplace. To load the plugin from a
local checkout:

1. Copy this `cursor-blog` folder into your Cursor local plugins directory:

   ```bash
   mkdir -p ~/.cursor/plugins/local
   cp -r plugins/cursor-blog ~/.cursor/plugins/local/cursor-blog
   ```

2. Restart Cursor, or run `Developer: Reload Window`.
3. **Verify discoverability** (only a real Cursor client can do this; it cannot be
   done from a cloud VM or CI): open Customize and confirm `Cursor Blog` and its
   sub-skills appear under Skills. Typing `/` in Agent chat should also list them.
   Local plugin imports must be allowed in your Cursor settings (on Teams and
   Enterprise, an admin controls "Allow Local Plugin Imports").

Alternatively, import the whole repository from GitHub: in Customize, choose
"From GitHub Repository". The root `.cursor-plugin/marketplace.json` lists this
plugin so Cursor can index it.

Publishing to the Cursor Marketplace is optional and can be done later by
submitting the repository to the Cursor team.

## Use it

Describe the task in natural language, or type `/` in Agent chat and pick a
skill. For example: "Write a blog post about X and score it", or
"SEO check this file". Each `skills/*/SKILL.md` `description` carries the trigger
phrases Cursor uses to decide when a skill applies.

For the exact helper-script overrides and the CLI commands, see the "Running in
Cursor" section of `skills/blog/SKILL.md` and the repository `CURATION.md`.
