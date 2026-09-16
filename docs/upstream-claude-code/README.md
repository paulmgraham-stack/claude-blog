# Upstream Claude Code reference (quarantine index)

This directory documents the parts of the repository that are **Claude Code
specific** and are therefore **not** part of the Cursor / Grok Bot curated
surface. Nothing was moved here; the files stay in their original locations so
this fork remains a low-drift mirror of
[`AgriciDaniel/claude-blog`](https://github.com/AgriciDaniel/claude-blog) and so
the upstream test suite keeps passing. This page is the map to them.

For the full curation rationale and the list of Cursor-ready parts, see
[`../../CURATION.md`](../../CURATION.md).

## Claude Code only artifacts (kept in place, not the Cursor path)

| Path | What it is | Why it is Claude Code specific |
|---|---|---|
| `install.sh`, `install.ps1` | Installers | Copy skills, agents, and scripts into the `~/.claude` tree so Claude Code can discover them. Cursor does not use `~/.claude`. |
| `uninstall.sh`, `uninstall.ps1` | Uninstallers | Remove the `~/.claude` install created above. |
| `.claude-plugin/plugin.json` | Plugin manifest | Describes the suite to the Claude Code plugin system. |
| `.claude-plugin/marketplace.json` | Marketplace catalog | Lists the plugin for Claude Code marketplace distribution. |
| `agents/*.md` | Subagents | Use the Claude Code subagent format (`tools:` frontmatter, dispatched via the Task tool). Kept as readable role specifications. |
| `brain/` | Vendored Obsidian brain | Upstream content-provenance and authoring tool. It is explicitly not part of the plugin payload and is not used by the skill surface. |

## Claude Code only workflows

- **Plugin install.** Upstream's recommended install copies files into
  `~/.claude` via the installer scripts, or adds the plugin through the Claude
  Code marketplace. In Cursor there is no install step: skills are read from
  `skills/**/SKILL.md` in place.
- **`/blog` slash commands.** Upstream exposes every sub-skill as a `/blog X`
  slash command with an `argument-hint`. In Cursor you invoke skills by natural
  language; the routing table in `skills/blog/SKILL.md` still serves as the
  capability map.
- **`claude plugin validate .`.** The CI `validate-skills` job installs the
  Claude Code CLI and validates the plugin packaging. It is not applicable to the
  Cursor use case and is left unmodified as upstream reference.

## How to consume these in Cursor instead

You do not need any of the above to use the blog and SEO skills in Cursor. Read
the relevant `skills/*/SKILL.md`, describe the task in natural language, and run
the `scripts/*.py` tooling directly. See the "How to use the curated set in
Cursor" section of [`../../CURATION.md`](../../CURATION.md).
