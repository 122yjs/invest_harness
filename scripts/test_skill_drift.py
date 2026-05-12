#!/usr/bin/env python3
"""Detect generated-layer drift against the invest research source layer."""

from __future__ import annotations

from pathlib import Path

from sync_invest_skills import (
    AGENT_PLUGIN_ROOT,
    AGENTS_ROOT,
    SOURCE_ROOT,
    add_generated_notice,
    repo_relative,
    source_files,
)


def test_generated_tree(
    source_directory: Path, destination_directories: list[Path], kind: str
) -> list[str]:
    failures: list[str] = []
    if not source_directory.is_dir():
        return [f"source directory missing: {repo_relative(source_directory)}"]

    expected_relative_paths: set[Path] = set()

    for source_file in source_files(source_directory):
        relative_to_tree = source_file.relative_to(source_directory)
        expected_relative_paths.add(relative_to_tree)

        source_relative = repo_relative(source_file)
        expected = add_generated_notice(
            source_file.read_text(encoding="utf-8"),
            source_relative,
            kind,
        )

        for destination_directory in destination_directories:
            destination_path = destination_directory / relative_to_tree
            if not destination_path.is_file():
                failures.append(f"missing generated {kind}: {repo_relative(destination_path)}")
                continue

            actual = destination_path.read_text(encoding="utf-8")
            if actual != expected:
                failures.append(
                    "drift detected in generated "
                    f"{kind}: {repo_relative(destination_path)} (source: {source_relative})"
                )

    for destination_directory in destination_directories:
        if not destination_directory.is_dir():
            failures.append(f"generated directory missing: {repo_relative(destination_directory)}")
            continue

        generated_files = sorted(
            path
            for path in destination_directory.rglob("*")
            if path.is_file() and path.name != ".DS_Store"
        )
        for generated_file in generated_files:
            relative_to_destination = generated_file.relative_to(destination_directory)
            if relative_to_destination not in expected_relative_paths:
                failures.append(
                    "stale generated "
                    f"{kind} not present in source: {repo_relative(generated_file)}"
                )

    return failures


def collect_failures() -> list[str]:
    failures: list[str] = []
    failures.extend(
        test_generated_tree(
            SOURCE_ROOT / "skills",
            [AGENT_PLUGIN_ROOT / "skills", AGENTS_ROOT / "skills"],
            "skill",
        )
    )
    failures.extend(
        test_generated_tree(
            SOURCE_ROOT / "commands",
            [AGENT_PLUGIN_ROOT / "commands", AGENTS_ROOT / "commands"],
            "command",
        )
    )
    failures.extend(
        test_generated_tree(
            SOURCE_ROOT / "policies",
            [AGENT_PLUGIN_ROOT / "policies", AGENTS_ROOT / "policies"],
            "policy",
        )
    )
    failures.extend(
        test_generated_tree(
            SOURCE_ROOT / "templates",
            [AGENT_PLUGIN_ROOT / "templates"],
            "template",
        )
    )
    return failures


def main() -> int:
    failures = collect_failures()
    if failures:
        print("Invest skill drift check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Invest skill drift check passed: generated layers match vertical source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

