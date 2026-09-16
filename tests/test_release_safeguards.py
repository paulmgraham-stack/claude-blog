"""Regression coverage for v2.2.0 release and repository safeguards."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def preflight_module():
    return _load_module("release_preflight", ROOT / "scripts" / "blog_preflight.py")


def test_has_module_handles_missing_dotted_parent(monkeypatch, preflight_module) -> None:
    def missing_parent(_name: str):
        raise ModuleNotFoundError("missing parent")

    monkeypatch.setattr(preflight_module.importlib.util, "find_spec", missing_parent)
    assert preflight_module._has_module("missing.child") is False


def test_has_module_handles_module_with_unset_spec(monkeypatch, preflight_module) -> None:
    def unset_spec(_name: str):
        raise ValueError("module.__spec__ is None")

    monkeypatch.setattr(preflight_module.importlib.util, "find_spec", unset_spec)
    assert preflight_module._has_module("loaded_without_spec") is False


def test_pagespeed_response_populates_audit_details(monkeypatch) -> None:
    scripts_dir = ROOT / "skills" / "blog-google" / "scripts"
    sys.path.insert(0, str(scripts_dir))
    try:
        module = _load_module("release_pagespeed", scripts_dir / "pagespeed_check.py")
    finally:
        sys.path.pop(0)

    class Response:
        status_code = 200
        text = ""

        @staticmethod
        def raise_for_status() -> None:
            return None

        @staticmethod
        def json() -> dict:
            return {
                "analysisUTCTimestamp": "2026-07-23T00:00:00Z",
                "lighthouseResult": {
                    "categories": {},
                    "audits": {
                        "image-delivery-insight": {
                            "title": "Improve image delivery",
                            "score": 0.5,
                            "details": {
                                "type": "table",
                                "headings": [{"key": "url"}],
                                "items": [{"url": "https://example.com/hero.jpg"}],
                            },
                        }
                    },
                },
            }

    monkeypatch.setattr(module, "request_with_retries", lambda *_a, **_kw: Response())
    result = module.run_pagespeed("https://example.com")
    assert result["error"] is None
    assert result["audit_details"]["image-delivery-insight"]["total_items"] == 1


def test_docs_have_no_active_powershell_pipe_to_execution() -> None:
    pattern = re.compile(
        r"(?:\birm\b|\bInvoke-RestMethod\b)[^\n]*\|\s*(?:iex|Invoke-Expression)\b",
        re.IGNORECASE,
    )
    violations = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        if pattern.search(path.read_text(encoding="utf-8")):
            violations.append(path.relative_to(ROOT).as_posix())
    assert not violations, f"active PowerShell pipe-to-execution instructions: {violations}"


def test_docs_have_no_active_shell_download_to_execution() -> None:
    pattern = re.compile(
        r"(?:\bcurl\b|\bwget\b)[^\n]*\|\s*(?:bash|sh)\b",
        re.IGNORECASE,
    )
    violations = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        if pattern.search(path.read_text(encoding="utf-8")):
            violations.append(path.relative_to(ROOT).as_posix())
    assert not violations, f"active shell download-to-execution instructions: {violations}"


def test_workflows_pin_reviewed_action_releases_by_sha() -> None:
    workflows = tuple(sorted((ROOT / ".github" / "workflows").glob("*.yml")))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in workflows)

    expected = {
        "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
        "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    }
    for action, sha in expected.items():
        refs = set(re.findall(rf"{re.escape(action)}@([^\s#]+)", combined))
        assert refs == {sha}, f"unreviewed {action} refs: {sorted(refs)}"


def test_editorial_guidance_has_no_stat_or_length_delivery_quotas() -> None:
    template_paths = (
        "news-analysis.md",
        "faq-knowledge.md",
        "data-research.md",
        "comparison.md",
        "tutorial.md",
        "case-study.md",
    )
    stat_quota = re.compile(
        r"(?:at least|minimum)\s+(?:one|\d+)[^\n]*(?:\[STAT\]|statistic)",
        re.IGNORECASE,
    )
    for name in template_paths:
        text = (ROOT / "skills" / "blog" / "templates" / name).read_text(
            encoding="utf-8"
        )
        assert not stat_quota.search(text), f"hard statistic quota remains in {name}"

    orchestrator = (ROOT / "skills" / "blog" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    outline = (ROOT / "skills" / "blog-outline" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "canonical target word count" not in orchestrator.lower()
    assert "never changes a score or blocks" in orchestrator
    assert "never score or block" in outline


def test_first_hand_and_retrieval_guidance_remains_evidence_conditional() -> None:
    brief = (ROOT / "skills" / "blog-brief" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    synthesis = (
        ROOT / "skills" / "blog" / "references" / "synthesis-contract.md"
    ).read_text(encoding="utf-8")
    research = (
        ROOT / "skills" / "blog" / "references" / "research-quality.md"
    ).read_text(encoding="utf-8")

    assert "only when the user supplies supporting methodology" in brief
    assert "retrieval notes required by FLOW" not in synthesis
    assert "retrieval notes required by FLOW" not in research


def test_editorial_heuristics_do_not_reward_fixed_passages_or_faq() -> None:
    guidance = (
        ROOT / "skills" / "blog" / "references" / "editorial-heuristics.md"
    ).read_text(encoding="utf-8")

    assert "about 50-word direct-answer" not in guidance
    assert "120 to 180 word citable passage" not in guidance
    assert "missing FAQ" not in guidance
    assert "Q&A presence and passage length earn no points" in guidance
    assert "intent-appropriate openings" in guidance


def test_active_templates_do_not_require_faq_counts_or_market_stat_openers() -> None:
    template_dir = ROOT / "skills" / "blog" / "templates"
    paths = [*sorted(template_dir.glob("*.md")), ROOT / "docs" / "TEMPLATES.md"]
    fixed_faq_count = re.compile(
        r"(?:FAQ|Q&A)[^\n]*\(\s*\d+(?:-\d+)?\s*(?:questions?|items?)",
        re.IGNORECASE,
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not fixed_faq_count.search(text), (
            f"fixed FAQ count remains in {path.relative_to(ROOT)}"
        )
        assert "At least 12 total questions" not in text
        assert "Only 3 questions" not in text

    listicle = (template_dir / "listicle.md").read_text(encoding="utf-8")
    assert "Open with the single most important market statistic" not in listicle
    assert "a market statistic only when it is material and sourced" in listicle


def test_length_experience_and_style_diagnostics_are_conditional() -> None:
    quality = (
        ROOT / "skills" / "blog" / "references" / "quality-scoring.md"
    ).read_text(encoding="utf-8")
    eeat = (
        ROOT / "skills" / "blog" / "references" / "eeat-signals.md"
    ).read_text(encoding="utf-8")

    assert "Paragraphs > 200 words (Yoast red)" not in quality
    assert "length alone does not set priority" in quality
    assert "never from length alone" in quality
    assert "needs first-hand testing" not in eeat
    assert "neutral sourced analysis can rely on" in eeat


def test_evidence_guidance_has_no_placement_or_source_count_quotas() -> None:
    troubleshooting = (ROOT / "docs" / "TROUBLESHOOTING.md").read_text(
        encoding="utf-8"
    )
    scorer = (ROOT / "scripts" / "ai_citation_score.py").read_text(
        encoding="utf-8"
    )

    assert "must be in the FIRST paragraph" not in troubleshooting
    assert "**Incorrect pattern** (stat buried)" not in troubleshooting
    assert "where it best supports\ncomprehension" in troubleshooting
    assert "at least three unique tier 1 or tier 2 citations" not in scorer
    assert "source count and diversity only when the topic" in scorer


def test_pillar_and_quality_gate_source_only_material_numeric_claims() -> None:
    pillar = (
        ROOT / "skills" / "blog" / "templates" / "pillar-page.md"
    ).read_text(encoding="utf-8")
    orchestrator = (ROOT / "skills" / "blog" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "Include at least one data point per core section" not in pillar
    assert "only when\nit materially improves the section" in pillar
    assert "Every number must have a named source" not in orchestrator
    assert "Source material factual statistics, measurements" in orchestrator
    assert "do not need redundant inline sourcing" in orchestrator


def test_quality_gate_default_threshold_is_seventy() -> None:
    quality_gate = (ROOT / "scripts" / "quality_gate.py").read_text(
        encoding="utf-8"
    )
    assert "DEFAULT_THRESHOLD = 70" in quality_gate


def test_rendering_guidance_accepts_valid_google_rendered_dom() -> None:
    analyzer = (ROOT / "skills" / "blog-analyze" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    crawler = (
        ROOT / "skills" / "blog" / "references" / "ai-crawler-guide.md"
    ).read_text(encoding="utf-8")

    assert "rendered DOM exposes consistent visible content and valid schema" in analyzer
    assert "not unconditional requirements" in analyzer
    assert "SSR/SSG, no JS-gated content" not in analyzer
    assert "single most common reason" not in crawler
    assert "test the deployed response" in crawler
    assert "not unconditional Google pass criteria" in crawler


def test_dependency_requirements_and_locks_are_coherent() -> None:
    audio_req = (
        ROOT / "skills" / "blog-audio" / "scripts" / "requirements.txt"
    ).read_text(encoding="utf-8")
    audio_lock = (
        ROOT / "skills" / "blog-audio" / "scripts" / "requirements.lock"
    ).read_text(encoding="utf-8")
    notebook_req = (
        ROOT / "skills" / "blog-notebooklm" / "scripts" / "requirements.txt"
    ).read_text(encoding="utf-8")
    notebook_lock = (
        ROOT / "skills" / "blog-notebooklm" / "scripts" / "requirements.lock"
    ).read_text(encoding="utf-8")
    google_req = (
        ROOT / "skills" / "blog-google" / "scripts" / "requirements.txt"
    ).read_text(encoding="utf-8")
    google_lock = (
        ROOT / "skills" / "blog-google" / "scripts" / "requirements.lock"
    ).read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    uv_lock = (ROOT / "uv.lock").read_text(encoding="utf-8")

    assert "google-genai>=2.14.0,<3.0.0" in audio_req
    assert "google-genai==2.14.0" in audio_lock
    assert '"google-genai>=2.14.0,<3.0.0"' in pyproject
    assert "patchright==1.61.2" in notebook_req
    assert "patchright==1.61.2" in notebook_lock
    assert '"patchright==1.61.2"' in pyproject
    assert 'name = "google-genai"\nversion = "2.14.0"' in uv_lock
    assert 'name = "patchright"\nversion = "1.61.2"' in uv_lock
    assert "google-ads>=31.2.0,<32.0.0" in google_req
    assert "google-ads==31.4.0" in google_lock
    assert '"google-ads>=31.2.0,<32.0.0"' in pyproject
    assert 'name = "google-ads"\nversion = "31.4.0"' in uv_lock


def test_google_update_ledger_is_present() -> None:
    assert (ROOT / "data" / "google-updates.json").is_file()


def test_dependency_smoke_cli_is_explicit_and_offline() -> None:
    script = (ROOT / "scripts" / "dependency_smoke.py").read_text(
        encoding="utf-8"
    )
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    for component in ("audio", "browser", "preflight"):
        assert f'"{component}"' in script
    assert "--require-hashes" in workflow
    assert "skills/blog-audio/scripts/requirements.lock" in workflow
    assert "skills/blog-notebooklm/scripts/requirements.lock" in workflow
    assert "--component audio" in workflow
    assert "--component browser --component preflight" in workflow
    assert "browser_launched" in script and "network_used" in script
    assert "generate_single_speaker" in script
    assert "tts_path_exercised" in script
    assert "response_modalities" in script
    assert "inline_pcm_verified" in script


def test_ledger_consumer_guidance_references_ledger() -> None:
    orchestrator = (ROOT / "skills" / "blog" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    currentness = (
        ROOT
        / "skills"
        / "blog-google"
        / "references"
        / "search-currentness.md"
    ).read_text(encoding="utf-8")

    for guidance in (orchestrator, currentness):
        assert "data/google-updates.json" in guidance


def _write_flow_lock(root: Path, content: bytes = b"prompt\n") -> None:
    prompt = (
        root
        / "skills"
        / "blog-flow"
        / "references"
        / "prompts"
        / "find"
        / "prompt.md"
    )
    prompt.parent.mkdir(parents=True)
    prompt.write_bytes(content)
    lock = root / "skills" / "blog-flow" / "references" / "flow-prompts.lock"
    lock.write_text(
        f"{hashlib.sha256(content).hexdigest()}  "
        "skills/blog-flow/references/prompts/find/prompt.md\n",
        encoding="utf-8",
    )


def test_consistency_checker_errors_on_missing_target_and_warns_on_orphan(
    tmp_path: Path,
) -> None:
    module = _load_module(
        "release_consistency", ROOT / "scripts" / "consistency_check.py"
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text(
        "[missing](missing.md)\n", encoding="utf-8"
    )
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "orphan.py").write_text(
        '"""fixture"""\n', encoding="utf-8"
    )
    _write_flow_lock(tmp_path)

    report = module.check(tmp_path)
    assert report["status"] == "fail"
    assert any(e["kind"] == "missing_markdown_target" for e in report["errors"])
    assert any(w["target"] == "scripts/orphan.py" for w in report["warnings"])


def test_consistency_checker_discovers_skill_relative_resources_and_agents(
    tmp_path: Path,
) -> None:
    module = _load_module(
        "release_consistency_relative",
        ROOT / "scripts" / "consistency_check.py",
    )
    skill = tmp_path / "skills" / "blog-demo"
    (skill / "references").mkdir(parents=True)
    (skill / "scripts").mkdir()
    (skill / "templates").mkdir()
    (skill / "SKILL.md").write_text(
        "Use `references/guide.md`, run `scripts/run.py`, load "
        "`templates/example.md`, then dispatch `blog-demo-agent`.\n",
        encoding="utf-8",
    )
    for relative in (
        "references/guide.md",
        "scripts/run.py",
        "templates/example.md",
    ):
        (skill / relative).write_text("fixture\n", encoding="utf-8")
    (tmp_path / "agents").mkdir()
    (tmp_path / "agents" / "blog-demo-agent.md").write_text(
        "agent\n", encoding="utf-8"
    )
    _write_flow_lock(tmp_path)

    report = module.check(tmp_path)
    warned = {entry["target"] for entry in report["warnings"]}
    assert report["status"] == "pass"
    assert "skills/blog-demo/references/guide.md" not in warned
    assert "skills/blog-demo/scripts/run.py" not in warned
    assert "skills/blog-demo/templates/example.md" not in warned
    assert "agents/blog-demo-agent.md" not in warned


def test_public_triage_note_covers_entire_open_backlog() -> None:
    path = ROOT / "docs" / "PUBLIC-BACKLOG-TRIAGE-2026-07-23.md"
    if not path.exists():
        pytest.skip("private-only triage note is excluded from public releases")
    text = path.read_text(encoding="utf-8")
    for number in (48, 47, 46, 42, 41, 40, 38, 37, 26, 25, 23, 20, 19, 18, 17, 15, 13, 10):
        assert f"/pull/{number}" in text
    for number in (44, 36, 33, 29, 22):
        assert f"/issues/{number}" in text
    assert "No public mutations were performed" in text
