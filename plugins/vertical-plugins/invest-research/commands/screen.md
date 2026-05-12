---
name: screen
command: /screen
maps_to_skill: idea-screener
thin_wrapper: true
status: scaffold-only
---

# /screen

Thin command stub for idea screening.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the screen prompt, constraints, and `${ACTIVE_WORKSPACE}` to the future `idea-screener` skill.
- Record that product screening logic is deferred to the skill implementation pass.

## Prohibited

- Do not rank stocks, calculate scores, or generate investment theses inside this command.
- Do not implement phase-2 screening logic here.

