---
name: earnings-update
description: Scaffold-only skill target for future earnings update workflows; command stubs may route here but first-pass infrastructure must not implement earnings analysis logic.
---

# earnings-update

## Status

This is a first-pass scaffold so `/earnings` has a real skill target.

## Boundary

- Use `${ACTIVE_WORKSPACE}` for any future output path.
- Do not fetch filings, calculate beat/miss, revise ratings, or summarize guidance in the infrastructure-freeze pass.
- Future implementation should write earnings artifacts under `${ACTIVE_WORKSPACE}/00_input/` or a dedicated dynamic workspace subfolder defined by the next pass.

## Deferred Workflow

The actual earnings update workflow is deferred to the next product-logic pass.

