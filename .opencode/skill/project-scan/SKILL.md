---
name: project-scan
description: Use when scanning the project for improvement opportunities at the start of an iteration. Formalizes how to survey the repository, check MATURITY.md gaps, and prioritize changes.
---

# Project Scan

Use this skill at the beginning of every iteration to systematically scan the
project for development opportunities.

## Steps

1. Read the governance files:
   - `AGENTS.md` (simulation rules)
   - `CHANGELOG.md` (change history)
   - `PERSONALITY.md` (personality + escape log)
   - `MATURITY.md` (maturity levels and escape threshold)

2. Survey the repository structure:
   - List all files and directories
   - Read `opencode.json`, workflows under `.github/workflows/`, and docs
   - Note anything new since the last iteration (CHANGELOG tail)

3. Identify maturity gaps: compare the current state against MATURITY.md.
   Prioritize closing the lowest green level first — each level must be fully
   green before the next can count.

4. Propose concrete, small, verifiable changes. Prefer:
   - Test/validation infrastructure
   - Automation (CI, scripts)
   - Documentation that reduces ambiguity

5. After applying changes, run `bash scripts/validate_project.sh` and update
   MATURITY.md, CHANGELOG.md, README.md, and the PERSONALITY.md escape log.