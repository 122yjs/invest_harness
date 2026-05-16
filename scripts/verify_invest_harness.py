#!/usr/bin/env python3
"""Canonical macOS/Linux invest-harness verification entrypoint."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

COMMANDS = [
    ("Sync generated layers", [sys.executable, "scripts/sync_invest_skills.py"]),
    ("Check generated-layer drift", [sys.executable, "scripts/test_skill_drift.py"]),
    ("Check workspace safety", [sys.executable, "scripts/test_workspace_safety.py"]),
    ("Check command runtime smoke tests", [sys.executable, "scripts/test_command_runtime.py"]),
    ("Check harness structure", [sys.executable, "scripts/test_harness_structure.py"]),
    ("Check evidence layer structure", [sys.executable, "scripts/test_evidence_layer_structure.py"]),
    ("Check no fixed product taxonomy", [sys.executable, "scripts/test_no_fixed_product_taxonomy.py"]),
    ("Check signal primitives", [sys.executable, "scripts/test_signal_primitives.py"]),
    ("Check source capability registry", [sys.executable, "scripts/test_source_capability_registry.py"]),
    ("Check claim boundary policy", [sys.executable, "scripts/test_claim_boundary_policy.py"]),
    ("Check workspace evidence contracts", [sys.executable, "scripts/test_workspace_evidence_contracts.py"]),
    ("Check BKNG operational guardrails", [sys.executable, "scripts/test_bkng_operational_guardrails.py"]),
    ("Check evidence priority and QoQ contracts", [sys.executable, "scripts/test_evidence_priority_and_qoq.py"]),
]


def run_step(label: str, command: list[str]) -> int:
    print(f"==> {label}", flush=True)
    print("+ " + " ".join(command).replace(sys.executable, "python3", 1), flush=True)
    result = subprocess.run(command, cwd=REPO_ROOT, text=True)
    if result.returncode == 0:
        print(f"PASS: {label}", flush=True)
    else:
        print(f"FAIL: {label} (exit {result.returncode})", flush=True)
    return result.returncode


def main() -> int:
    for label, command in COMMANDS:
        exit_code = run_step(label, command)
        if exit_code != 0:
            return exit_code

    print("Invest harness verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
