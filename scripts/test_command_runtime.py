#!/usr/bin/env python3
"""Smoke tests for the invest command runtime parser and dispatcher."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from invest_command_runtime import dispatch_command


SMOKE_COMMANDS = [
    (
        "/screen AI 전력 인프라 2차 수혜주",
        "screen",
        "idea-screener",
        "${ACTIVE_WORKSPACE}/00_screen/shortlist.md",
    ),
    (
        "/earnings TSLA Q1 2026",
        "earnings",
        "earnings-update",
        "${ACTIVE_WORKSPACE}/00_input/earnings-update.md",
    ),
    (
        "/comps AAPL peers MSFT NVDA",
        "comps",
        "valuation-analyst",
        "${ACTIVE_WORKSPACE}/03_valuation/comps.md",
    ),
    (
        "/dcf AAPL base",
        "dcf",
        "valuation-analyst",
        "${ACTIVE_WORKSPACE}/03_valuation/dcf.md",
    ),
    (
        "/qa report.md",
        "qa",
        "qa-reviewer",
        "${ACTIVE_WORKSPACE}/09_qa/final-check.md",
    ),
    (
        "/preview NVDA",
        "preview",
        "earnings-preview",
        "${ACTIVE_WORKSPACE}/00_input/earnings-preview.md",
    ),
    (
        "/sector AI 전력 인프라",
        "sector",
        "sector-analyst",
        "${ACTIVE_WORKSPACE}/02_fundamental/sector.md",
    ),
    (
        "/thesis CSTM",
        "thesis",
        "thesis-tracker",
        "${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md",
    ),
    (
        "/catalysts AI 전력 인프라 next 3 months",
        "catalysts",
        "catalyst-tracker",
        "${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md",
    ),
    (
        "/report-html AAPL",
        "report-html",
        "html-report-synthesizer",
        "${ACTIVE_WORKSPACE}/08_final/report.html",
    ),
    (
        "/morning-note AI 반도체",
        "morning-note",
        "morning-note",
        "${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md",
    ),
    (
        "/update AAPL earnings",
        "update",
        "report-updater",
        "${ACTIVE_WORKSPACE}/00_input/update-plan.md",
    ),
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_smoke_commands() -> None:
    with tempfile.TemporaryDirectory(prefix="invest-command-runtime-") as temp_dir:
        workspace_base = Path(temp_dir)
        for raw_command, command_name, skill_name, required_output in SMOKE_COMMANDS:
            payload = dispatch_command(
                raw_command,
                workspace_base=workspace_base,
                run_date="20260513",
            )
            workspace = Path(str(payload["active_workspace"]))
            dispatch_file = workspace / "00_input" / "command-dispatch.json"

            assert_true(payload["command"] == command_name, f"command mismatch: {raw_command}")
            assert_true(
                payload["maps_to_skill"] == skill_name,
                f"skill mapping mismatch: {raw_command}",
            )
            assert_true(payload["thin_wrapper"] is True, f"not thin wrapper: {raw_command}")
            assert_true(workspace.is_dir(), f"workspace missing: {workspace}")
            assert_true(dispatch_file.is_file(), f"dispatch file missing: {dispatch_file}")
            assert_true(
                required_output in payload["expected_outputs"],
                f"required output missing from payload: {required_output}",
            )

            persisted = json.loads(dispatch_file.read_text(encoding="utf-8"))
            assert_true(
                persisted["runtime_contract"] == "dispatch-only",
                f"runtime contract mismatch: {dispatch_file}",
            )
            assert_true(
                persisted["active_workspace"] == workspace.as_posix(),
                f"persisted workspace mismatch: {dispatch_file}",
            )


def test_workspace_collision_suffix() -> None:
    with tempfile.TemporaryDirectory(prefix="invest-command-runtime-") as temp_dir:
        workspace_base = Path(temp_dir)
        first = dispatch_command("/screen AI infrastructure", workspace_base=workspace_base, run_date="20260513")
        second = dispatch_command("/screen AI infrastructure", workspace_base=workspace_base, run_date="20260513")

        assert_true(
            first["active_workspace"] != second["active_workspace"],
            "second run should not overwrite an existing workspace",
        )
        assert_true(
            Path(str(first["active_workspace"])).is_dir()
            and Path(str(second["active_workspace"])).is_dir(),
            "collision workspaces should both exist",
        )


def main() -> int:
    test_smoke_commands()
    test_workspace_collision_suffix()
    print(
        "Command runtime smoke tests passed: parser, skill dispatch, "
        "ACTIVE_WORKSPACE creation, and collision suffixing are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
