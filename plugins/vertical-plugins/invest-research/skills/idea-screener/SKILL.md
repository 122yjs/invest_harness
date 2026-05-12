---
name: idea-screener
description: Scaffold-only skill target for future screening workflows; command stubs may route here but first-pass infrastructure must not implement screening logic.
---

# idea-screener

## Status

This is a first-pass scaffold so `/screen` has a real skill target.

## Boundary

- Use `${ACTIVE_WORKSPACE}` for any future output path.
- Do not rank securities, calculate idea scores, or generate investment theses in the infrastructure-freeze pass.
- Future implementation should write screening artifacts under `${ACTIVE_WORKSPACE}/00_screen/`.

## Deferred Workflow

The actual idea screening workflow is deferred to the next product-logic pass.

