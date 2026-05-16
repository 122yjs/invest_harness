#!/usr/bin/env python3
"""Validate dynamic workspace rules for invest-harness docs and runtime surfaces."""

from __future__ import annotations

import re
from pathlib import Path

from sync_invest_skills import REPO_ROOT, repo_relative

SCAN_ROOTS = [
    "AGENTS.md",
    "README.md",
    "docs/harness/invest",
    "plugins/vertical-plugins/invest-research",
    "plugins/agent-plugins/invest-harness",
    ".agents/skills",
    ".agents/commands",
    ".agents/policies",
    "scripts",
]

LEGACY_WORKSPACE = REPO_ROOT / "_workspace"
FIXED_WORKSPACE_PATTERN = re.compile(r"(?<![A-Za-z0-9])_workspace[\\/]")
ACTIVE_WORKSPACE_PATTERN = re.compile(r"\$\{ACTIVE_WORKSPACE\}")


def scannable_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        absolute_root = REPO_ROOT / root
        if not absolute_root.exists():
            continue
        if absolute_root.is_file():
            files.append(absolute_root)
            continue
        for path in absolute_root.rglob("*"):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            try:
                path.relative_to(LEGACY_WORKSPACE)
                continue
            except ValueError:
                files.append(path)
    return sorted(files)


def collect_failures() -> list[str]:
    failures: list[str] = []

    for path in scannable_files():
        content = path.read_text(encoding="utf-8")
        matches = FIXED_WORKSPACE_PATTERN.findall(content)
        if matches:
            failures.append(
                f"fixed legacy workspace path found in {repo_relative(path)} "
                f"({len(matches)} occurrence(s))"
            )

    source_skill_root = REPO_ROOT / "plugins/vertical-plugins/invest-research/skills"
    for skill_file in sorted(source_skill_root.rglob("SKILL.md")):
        content = skill_file.read_text(encoding="utf-8")
        if not ACTIVE_WORKSPACE_PATTERN.search(content):
            failures.append(
                f"source skill does not reference ${{ACTIVE_WORKSPACE}}: {repo_relative(skill_file)}"
            )

    command_root = REPO_ROOT / "plugins/vertical-plugins/invest-research/commands"
    for command_file in sorted(command_root.rglob("*")):
        if not command_file.is_file():
            continue
        content = command_file.read_text(encoding="utf-8")
        if not ACTIVE_WORKSPACE_PATTERN.search(content):
            failures.append(
                f"command stub does not reference ${{ACTIVE_WORKSPACE}}: "
                f"{repo_relative(command_file)}"
            )
        if not re.search(r"thin_wrapper:\s*true", content):
            failures.append(
                f"command stub is missing thin_wrapper:true metadata: "
                f"{repo_relative(command_file)}"
            )

    return failures


def main() -> int:
    failures = collect_failures()

    if LEGACY_WORKSPACE.is_dir():
        print(f"Legacy sample workspace preserved and excluded: {repo_relative(LEGACY_WORKSPACE)}")
    else:
        print("Legacy sample workspace not present; nothing to preserve.")

    if failures:
        print("Workspace safety check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Workspace safety check passed: dynamic workspace rules are enforced for "
        "scanned docs, skills, commands, scripts, and templates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
