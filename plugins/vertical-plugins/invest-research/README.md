# Invest Research Vertical Plugin

This directory is the source layer for the invest harness.

- `skills/` contains hand-edited source skills.
- `commands/` contains thin command stubs.
- `policies/` contains common execution policies.
- `templates/` contains source templates shared by the generated runtime layers.

Generated runtime artifacts are produced by running `scripts/Sync-InvestSkills.sh` (macOS/Linux) or `scripts/Sync-InvestSkills.ps1` (Windows) which invoke `scripts/sync_invest_skills.py`.
Do not treat `.agents/skills/` as a source layer.

