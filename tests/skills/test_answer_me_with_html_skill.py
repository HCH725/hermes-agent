"""Behavior tests for the answer-me-with-html optional skill."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO / "optional-skills" / "web-development" / "answer-me-with-html"
SKILL_MD = SKILL_DIR / "SKILL.md"
RENDERER = SKILL_DIR / "scripts" / "am.mjs"
UPSTREAM_LICENSE = SKILL_DIR / "LICENSE.upstream"


def _frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "SKILL.md must start with YAML frontmatter"
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_skill_metadata_and_hermes_adapter():
    text = SKILL_MD.read_text(encoding="utf-8")
    frontmatter = _frontmatter(text)

    assert frontmatter["name"] == "answer-me-with-html"
    assert frontmatter["license"] == "MIT"
    assert "QingYunA" in frontmatter["author"]

    description = frontmatter["description"].strip('"')
    assert len(description) <= 60
    assert description.endswith(".")

    assert "${HERMES_SKILL_DIR}/scripts/am.mjs" in text
    assert "CLAUDE_SKILL_DIR" not in text
    assert "--no-open" in text
    assert "not always-on" in text
    assert RENDERER.is_file()
    assert UPSTREAM_LICENSE.is_file()


def test_required_sections_present():
    text = SKILL_MD.read_text(encoding="utf-8")
    for heading in (
        "## When to Use",
        "## Prerequisites",
        "## How to Run",
        "## Quick Reference",
        "## Procedure",
        "## Pitfalls",
        "## Verification",
    ):
        assert heading in text


def test_bundled_renderer_smoke(tmp_path: Path):
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js is not installed")

    output = tmp_path / "smoke.html"
    draft = """---
title: Smoke
---
## A Result
```callout ok Works
Hermes can render this page.
```
"""
    env = os.environ.copy()
    env["AM_HOME"] = str(tmp_path / "am-home")
    env["AM_NO_OPEN"] = "1"

    result = subprocess.run(
        [node, str(RENDERER), "render", "-", "--no-open", "-o", str(output)],
        input=draft,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("✓ ")
    html = output.read_text(encoding="utf-8")
    assert "<html" in html.lower()
    assert "Smoke" in html
