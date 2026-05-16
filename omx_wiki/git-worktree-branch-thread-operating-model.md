---
title: "Git Worktree Branch Thread Operating Model"
tags: ["git", "worktree", "branch", "codex-thread", "session", "goal-api", "workflow"]
created: 2026-05-13T22:40:12.132Z
updated: 2026-05-16T12:18:00.000Z
sources: []
links: []
category: reference
confidence: medium
schemaVersion: 1
---

# Git Worktree Branch Thread Operating Model

## Concepts

- Branch: repository-level history pointer. A repo can have many branches.
- Worktree: filesystem checkout attached to one repository. A single worktree can have only one branch checked out at a time.
- Codex thread/session: agent conversation and execution context. It is separate from Git branches and worktrees.
- Codex goal API thread: goal state is scoped to the active Codex thread, not to a Git worktree or branch.
- GitHub merge: depends on branch name, commits, target branch, conflicts, and CI. Local worktree folder names do not affect GitHub merge behavior.

## Safe Operating Rule

Use one clear work unit per substantial task:

```text
one worktree + one branch + one Codex thread + one ultragoal set
```

This prevents three common failures:

- editing in the wrong checkout because the Codex session cwd still points at `main`
- merging or pushing the wrong branch because the worktree folder name differs from the checked-out branch
- trying to reuse a Codex goal API thread that still carries an old goal state

## Project Convention

- Keep the root checkout on `main` for comparison and merge checks.
- Create new development lanes as **outside sibling folders** (e.g., `../project-branch`) relative to the main checkout. Do NOT use nested `.worktrees/` folders.
- *Why sibling?* Nested structures often confuse IDEs, search tools, backup systems, formatters, and AI agent sessions (sandbox permission boundaries).
- Keep the worktree folder name and branch name aligned whenever possible.
- Good sibling lane example: `../invest_harness-clean-dev2` with branch `dev2`.
- Good namespaced lane example: `../invest_harness-clean-refactor-20260514` with branch `codex/refactor-invest-harness-20260514`.
- Avoid misleading states such as `../invest_harness-clean-main-session` checked out on `codex/refactor-invest-harness-next-20260514`.

## Start Checklist

Before editing, run:

```bash
pwd
git branch --show-current
git status --short --branch
git worktree list --porcelain
```

Only proceed when the path, branch, and intended work lane match.

## Ultragoal Checklist

Before starting a new ultragoal in Codex:

- Prefer a fresh Codex thread/session for a fresh ultragoal set.
- Call `get_goal` in the active thread.
- Create a new Codex goal only when `get_goal` reports no active goal and the objective matches the current ultragoal handoff.
- Treat `.omx/ultragoal` as worktree/repo artifact state, and Codex goal API as thread state.

## Finish Checklist

Before claiming the lane is ready:

```bash
git status --short --branch
git worktree list --porcelain
python3 scripts/verify_invest_harness.py
```

For this project, `python3 scripts/verify_invest_harness.py` is the canonical macOS/Linux verifier.
