# Workspace Safety Policy

## Purpose

Every invest-harness run must write into one explicit active workspace. New workflow instructions must not target a fixed legacy workspace path.

## Required Active Workspace

- Bind `${ACTIVE_WORKSPACE}` before any skill writes research artifacts.
- Use a dynamic folder name such as `_workspace_AAPL_20260512/` or `_workspace_005930KS_20260512/` when a new run creates a folder.
- If the dynamic folder already exists, append a time suffix such as `_143022`.
- Pass the same `${ACTIVE_WORKSPACE}` value to every skill, command wrapper, synthesis step, and QA step.

## Legacy Sample Artifacts

Existing sample outputs in the repository-level legacy workspace are preserved as historical examples. The first-pass infrastructure freeze must not delete, move, rename, or reinterpret those files.

## Prohibited New Instructions

Do not instruct a skill, command, script, or template to write to a fixed legacy workspace path. Use `${ACTIVE_WORKSPACE}/03_valuation/findings.md` or a dynamic example instead.

## Verification

`scripts/Test-WorkspaceSafety.ps1` must fail when docs, skills, commands, scripts, or templates contain a fixed legacy workspace storage instruction outside the preserved sample artifact folder.

