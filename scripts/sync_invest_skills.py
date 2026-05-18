#!/usr/bin/env python3
"""Regenerate invest-harness runtime layers from the vertical source layer."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "plugins" / "vertical-plugins" / "invest-research"
AGENT_PLUGIN_ROOT = REPO_ROOT / "plugins" / "agent-plugins" / "invest-harness"
AGENTS_ROOT = REPO_ROOT / ".agents"

POLICY_NAMES = [
    "workspace-safety.md",
    "market-price-anchor.md",
    "data-source-policy.md",
    "qa-recalculation-policy.md",
    "rating-price-target-policy.md",
    "report-writing-style-policy.md",
]


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def assert_directory(path: Path, description: str) -> None:
    if not path.is_dir():
        raise SystemExit(f"Required directory missing: {description} ({path})")


def generated_notice(source_relative_path: str, kind: str) -> str:
    return (
        f"<!-- GENERATED-SYNC: source={source_relative_path}; kind={kind}; "
        "script=scripts/sync_invest_skills.py -->\n"
        "> [!IMPORTANT]\n"
        "> Generated execution artifact. Do not edit directly; edit the vertical source and rerun "
        "`python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).\n"
        "> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.\n"
        "> Runtime output paths must use `${ACTIVE_WORKSPACE}`.\n"
        "<!-- END GENERATED-SYNC -->\n"
    )


def add_generated_notice(content: str, source_relative_path: str, kind: str) -> str:
    normalized = content.replace("\r\n", "\n")
    notice = generated_notice(source_relative_path, kind)

    if normalized.startswith("---\n"):
        end = normalized.find("\n---\n", 4)
        if end != -1:
            frontmatter = normalized[: end + len("\n---\n")]
            body = normalized[end + len("\n---\n") :]
            return f"{frontmatter}\n{notice}\n{body}"

    return f"{notice}\n{normalized}"


def reset_generated_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def source_files(source_directory: Path) -> list[Path]:
    return sorted(
        path
        for path in source_directory.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    )


def sync_markdown_tree(
    source_directory: Path, destination_directories: list[Path], kind: str
) -> None:
    assert_directory(source_directory, f"{kind} source")

    for destination_directory in destination_directories:
        reset_generated_directory(destination_directory)

    for source_file in source_files(source_directory):
        relative_to_tree = source_file.relative_to(source_directory)
        source_relative = repo_relative(source_file)
        raw = source_file.read_text(encoding="utf-8")
        generated = add_generated_notice(raw, source_relative, kind)

        for destination_directory in destination_directories:
            destination_path = destination_directory / relative_to_tree
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            destination_path.write_text(generated, encoding="utf-8", newline="")
            print(f"synced {kind}: {source_relative} -> {repo_relative(destination_path)}")


def sync_invest_skills() -> None:
    assert_directory(SOURCE_ROOT, "vertical source root")

    for policy_name in POLICY_NAMES:
        policy_path = SOURCE_ROOT / "policies" / policy_name
        if not policy_path.is_file():
            raise SystemExit(
                "Required policy missing: "
                f"plugins/vertical-plugins/invest-research/policies/{policy_name}"
            )

    sync_markdown_tree(
        SOURCE_ROOT / "skills",
        [AGENT_PLUGIN_ROOT / "skills", AGENTS_ROOT / "skills"],
        "skill",
    )
    sync_markdown_tree(
        SOURCE_ROOT / "commands",
        [AGENT_PLUGIN_ROOT / "commands", AGENTS_ROOT / "commands"],
        "command",
    )
    sync_markdown_tree(
        SOURCE_ROOT / "policies",
        [AGENT_PLUGIN_ROOT / "policies", AGENTS_ROOT / "policies"],
        "policy",
    )
    sync_markdown_tree(
        SOURCE_ROOT / "templates",
        [AGENT_PLUGIN_ROOT / "templates"],
        "template",
    )

    print("Invest skill sync completed successfully.")


def main() -> int:
    sync_invest_skills()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

