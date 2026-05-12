---
name: screen
command: /screen
maps_to_skill: idea-screener
thin_wrapper: true
---

# /screen

Thin command stub for idea screening.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the screen prompt, constraints, market scope, and `${ACTIVE_WORKSPACE}` to `idea-screener`.
- Require `idea-screener` to write screening outputs under `${ACTIVE_WORKSPACE}/00_screen/`.

## Prohibited

- Do not rank stocks, calculate scores, or generate investment theses inside this command.
- Do not implement screening logic in the command wrapper.
