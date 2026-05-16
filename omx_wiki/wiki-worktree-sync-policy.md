---
title: "Wiki Worktree Sync Policy"
tags: ["wiki", "worktree", "git", "sync", "log", "workflow"]
created: 2026-05-16T13:45:00.000Z
updated: 2026-05-16T13:45:00.000Z
sources: []
links: ["git-worktree-branch-thread-operating-model.md"]
category: convention
confidence: high
schemaVersion: 1
---

# Wiki Worktree Sync Policy

## Rule

Treat wiki knowledge pages as Git-shared project knowledge:

```text
edit omx_wiki/*.md knowledge pages
-> commit on main or the chosen integration branch
-> merge/rebase other worktrees
```

## Worktree Behavior

- `omx_wiki/*.md` knowledge pages and `omx_wiki/index.md` are normal tracked Git objects.
- Two worktrees at the same commit have the same wiki body and index content.
- Worktree-specific drift can still appear when a local command updates execution traces such as `omx_wiki/log.md`.
- A dirty `omx_wiki/log.md` usually means "this worktree ran a wiki lifecycle command", not "the shared wiki knowledge diverged".

## Operating Guidance

- Commit durable wiki knowledge from the integration lane, then merge or rebase feature worktrees.
- Do not treat a local lint log entry as a knowledge conflict by itself.
- Before comparing wiki state across worktrees, separate durable knowledge files from command-run logs.
- For branch and worktree lane setup, follow [[git-worktree-branch-thread-operating-model.md]].
