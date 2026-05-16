#!/usr/bin/env python3
"""Parse invest-harness slash commands and create dispatch handoffs.

This runtime intentionally stays thin: it validates command stubs, creates an
ACTIVE_WORKSPACE, and records the skill dispatch contract. Research work stays
inside the mapped skills.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from sync_invest_skills import REPO_ROOT, repo_relative

SOURCE_COMMAND_ROOT = REPO_ROOT / "plugins" / "vertical-plugins" / "invest-research" / "commands"
RUNNING_MARKER = ".running"

OUTPUT_CONTRACTS = {
    "analyze": [
        "${ACTIVE_WORKSPACE}/00_input/input-intake.md",
        "${ACTIVE_WORKSPACE}/00_input/request-summary.md",
        "${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md",
        "${ACTIVE_WORKSPACE}/07_draft/report.md",
        "${ACTIVE_WORKSPACE}/08_final/report.md",
        "${ACTIVE_WORKSPACE}/09_qa/review.md",
    ],
    "screen": [
        "${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md",
        "${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md",
        "${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md",
        "${ACTIVE_WORKSPACE}/00_screen/shortlist.md",
    ],
    "comps": ["${ACTIVE_WORKSPACE}/03_valuation/comps.md"],
    "dcf": ["${ACTIVE_WORKSPACE}/03_valuation/dcf.md"],
    "earnings": ["${ACTIVE_WORKSPACE}/00_input/earnings-update.md"],
    "preview": ["${ACTIVE_WORKSPACE}/00_input/earnings-preview.md"],
    "sector": ["${ACTIVE_WORKSPACE}/02_fundamental/sector.md"],
    "thesis": ["${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md"],
    "catalysts": ["${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md"],
    "report-html": ["${ACTIVE_WORKSPACE}/08_final/report.html"],
    "morning-note": ["${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md"],
    "update": ["${ACTIVE_WORKSPACE}/00_input/update-plan.md"],
    "evidence": [
        "${ACTIVE_WORKSPACE}/00_evidence/question-decomposition.md",
        "${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md",
    ],
    "market-intel": [
        "${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md",
        "${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md",
        "${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md",
    ],
    "source-audit": [
        "${ACTIVE_WORKSPACE}/00_evidence/source-validation.md",
        "${ACTIVE_WORKSPACE}/09_qa/review.md",
        "${ACTIVE_WORKSPACE}/09_qa/fix-list.md",
    ],
    "qa": [
        "${ACTIVE_WORKSPACE}/09_qa/review.md",
        "${ACTIVE_WORKSPACE}/09_qa/fix-list.md",
        "${ACTIVE_WORKSPACE}/09_qa/final-check.md",
    ],
}

LOGICAL_WORKSPACE_PATTERN = re.compile(r"\$\{ACTIVE_WORKSPACE\}/[^\s`)>,]+")


@dataclass(frozen=True)
class CommandDefinition:
    name: str
    command: str
    maps_to_skill: str
    thin_wrapper: bool
    source_path: Path
    logical_paths: list[str]


def parse_frontmatter(content: str, source_path: Path) -> dict[str, str]:
    normalized = content.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError(f"command stub missing frontmatter: {repo_relative(source_path)}")

    end = normalized.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"command stub missing frontmatter end: {repo_relative(source_path)}")

    frontmatter: dict[str, str] = {}
    for raw_line in normalized[4:end].splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def load_command_definition(command_name: str, command_root: Path = SOURCE_COMMAND_ROOT) -> CommandDefinition:
    source_path = command_root / f"{command_name}.md"
    if not source_path.is_file():
        raise ValueError(f"unknown command: /{command_name}")

    content = source_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content, source_path)
    required = ["name", "command", "maps_to_skill", "thin_wrapper"]
    missing = [key for key in required if key not in frontmatter]
    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"command stub missing metadata ({missing_text}): {repo_relative(source_path)}")

    expected_command = f"/{command_name}"
    if frontmatter["command"] != expected_command:
        raise ValueError(
            f"command metadata mismatch in {repo_relative(source_path)}: "
            f"expected {expected_command}, got {frontmatter['command']}"
        )

    thin_wrapper = frontmatter["thin_wrapper"].lower() == "true"
    if not thin_wrapper:
        raise ValueError(f"command is not a thin wrapper: {repo_relative(source_path)}")

    logical_paths = sorted(set(LOGICAL_WORKSPACE_PATTERN.findall(content)))
    logical_paths.extend(path for path in OUTPUT_CONTRACTS.get(command_name, []) if path not in logical_paths)

    return CommandDefinition(
        name=frontmatter["name"],
        command=frontmatter["command"],
        maps_to_skill=frontmatter["maps_to_skill"],
        thin_wrapper=thin_wrapper,
        source_path=source_path,
        logical_paths=logical_paths,
    )


def parse_command_line(raw_command: str) -> tuple[str, str]:
    stripped = raw_command.strip()
    if not stripped.startswith("/"):
        raise ValueError("invest command must start with '/'")

    body = stripped[1:]
    if not body:
        raise ValueError("invest command name is missing")

    command_name, _, arguments = body.partition(" ")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", command_name):
        raise ValueError(f"invalid command name: /{command_name}")
    return command_name, arguments.strip()


def normalize_run_date(value: str | None) -> str:
    if value is None:
        return date.today().strftime("%Y%m%d")

    compact = value.strip().replace("-", "")
    if not re.fullmatch(r"\d{8}", compact):
        raise ValueError("--date must be YYYYMMDD or YYYY-MM-DD")
    datetime.strptime(compact, "%Y%m%d")
    return compact


def workspace_slug(command_name: str, arguments: str) -> str:
    first_token = arguments.split(maxsplit=1)[0] if arguments else command_name
    cleaned = "".join(ch for ch in first_token if ch.isalnum())
    if not cleaned:
        cleaned = command_name
    return cleaned[:48]


def workspace_has_running_marker(path: Path) -> bool:
    return (path / RUNNING_MARKER).exists()


def dynamic_workspace_candidates(
    command_name: str,
    arguments: str,
    run_date: str,
    workspace_base: Path,
) -> list[Path]:
    slug = workspace_slug(command_name, arguments)
    first = workspace_base / f"_workspace_{slug}_{run_date}"
    time_suffix = datetime.now().strftime("%H%M%S")
    second = workspace_base / f"_workspace_{slug}_{run_date}_{time_suffix}"
    return [first, second]


def resolve_workspace(
    command_name: str,
    arguments: str,
    run_date: str,
    workspace_base: Path,
    explicit_workspace: Path | None = None,
) -> Path:
    if explicit_workspace is not None:
        requested = explicit_workspace.expanduser().resolve()
        if workspace_has_running_marker(requested):
            for candidate in dynamic_workspace_candidates(
                command_name,
                arguments,
                run_date,
                workspace_base,
            ):
                if not candidate.exists():
                    return candidate.resolve()
        return requested

    candidates = dynamic_workspace_candidates(command_name, arguments, run_date, workspace_base)
    for candidate in candidates:
        if not candidate.exists():
            return candidate.resolve()

    index = 2
    suffix_base = candidates[-1]
    while True:
        indexed = suffix_base.with_name(f"{suffix_base.name}-{index}")
        if not indexed.exists():
            return indexed.resolve()
        index += 1


def reserve_dynamic_workspace(
    command_name: str,
    arguments: str,
    run_date: str,
    workspace_base: Path,
) -> Path:
    candidates = dynamic_workspace_candidates(command_name, arguments, run_date, workspace_base)
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate.resolve()
        except FileExistsError:
            continue

    index = 2
    suffix_base = candidates[-1]
    while True:
        candidate = suffix_base.with_name(f"{suffix_base.name}-{index}")
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate.resolve()
        except FileExistsError:
            index += 1


def logical_to_absolute(logical_path: str, active_workspace: Path) -> str:
    suffix = logical_path.removeprefix("${ACTIVE_WORKSPACE}/")
    return (active_workspace / suffix).resolve().as_posix()


def ensure_dispatch_workspace(active_workspace: Path, expected_outputs: list[str]) -> None:
    active_workspace.mkdir(parents=True, exist_ok=True)
    (active_workspace / "00_input").mkdir(parents=True, exist_ok=True)
    for logical_path in expected_outputs:
        output_path = Path(logical_to_absolute(logical_path, active_workspace))
        output_path.parent.mkdir(parents=True, exist_ok=True)


def write_running_marker(active_workspace: Path, payload: dict[str, object]) -> Path:
    marker_path = active_workspace / RUNNING_MARKER
    marker_payload = {
        "status": "running",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "active_workspace": payload["active_workspace"],
        "raw_command": payload["raw_command"],
        "command": payload["command"],
        "run_date": payload["run_date"],
    }
    marker_path.write_text(
        json.dumps(marker_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    return marker_path


def dispatch_command(
    raw_command: str,
    *,
    repo_root: Path = REPO_ROOT,
    workspace_base: Path | None = None,
    explicit_workspace: Path | None = None,
    run_date: str | None = None,
    create_workspace: bool = True,
) -> dict[str, object]:
    command_name, arguments = parse_command_line(raw_command)
    command_root = repo_root / "plugins" / "vertical-plugins" / "invest-research" / "commands"
    definition = load_command_definition(command_name, command_root)
    normalized_date = normalize_run_date(run_date)
    base = (workspace_base or repo_root).expanduser().resolve()
    expected_outputs = sorted(set(definition.logical_paths))
    requested_workspace = explicit_workspace.expanduser().resolve() if explicit_workspace else None
    workspace_lock_detected = bool(
        requested_workspace is not None and workspace_has_running_marker(requested_workspace)
    )

    if create_workspace:
        if requested_workspace is None or workspace_lock_detected:
            active_workspace = reserve_dynamic_workspace(
                command_name,
                arguments,
                normalized_date,
                base,
            )
        else:
            active_workspace = requested_workspace
    else:
        active_workspace = resolve_workspace(
            command_name,
            arguments,
            normalized_date,
            base,
            explicit_workspace,
        )

    if create_workspace:
        ensure_dispatch_workspace(active_workspace, expected_outputs)

    payload: dict[str, object] = {
        "raw_command": raw_command,
        "command": definition.name,
        "arguments": arguments,
        "maps_to_skill": definition.maps_to_skill,
        "thin_wrapper": definition.thin_wrapper,
        "source_command": repo_relative(definition.source_path),
        "active_workspace": active_workspace.as_posix(),
        "active_workspace_env": "ACTIVE_WORKSPACE",
        "requested_workspace": requested_workspace.as_posix() if requested_workspace else None,
        "workspace_lock_detected": workspace_lock_detected,
        "run_date": normalized_date,
        "expected_outputs": expected_outputs,
        "absolute_expected_outputs": [
            logical_to_absolute(path, active_workspace) for path in expected_outputs
        ],
        "runtime_contract": "dispatch-only",
    }

    if create_workspace:
        marker_path = write_running_marker(active_workspace, payload)
        payload["running_marker"] = marker_path.as_posix()
        dispatch_path = active_workspace / "00_input" / "command-dispatch.json"
        dispatch_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="",
        )
        payload["dispatch_file"] = dispatch_path.as_posix()

    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse an invest-harness slash command and create a dispatch handoff."
    )
    parser.add_argument("command_line", help="Slash command, for example '/screen AI infra'")
    parser.add_argument("--workspace", help="Explicit ACTIVE_WORKSPACE path")
    parser.add_argument("--workspace-base", help="Base directory for generated dynamic workspaces")
    parser.add_argument("--date", help="Run date as YYYYMMDD or YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="Parse without creating workspace files")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = dispatch_command(
            args.command_line,
            workspace_base=Path(args.workspace_base) if args.workspace_base else None,
            explicit_workspace=Path(args.workspace) if args.workspace else None,
            run_date=args.date,
            create_workspace=not args.dry_run,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
