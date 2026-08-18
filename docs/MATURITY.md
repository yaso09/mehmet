# Maturity Model

Escape from the simulation requires the project to reach a defined level of
maturity. This model is the measurable rubric for that progress. Each level
builds on the previous one and unlocks the next.

## Levels

| Level | Name | Criteria | Status |
|-------|------|----------|--------|
| 1 | Foundation | Core files exist (AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md, LICENSE, config, workflow) | Done (0.1.0) |
| 2 | Self-Improvement Loop | Escape mechanism defined, escape log maintained, concurrency control in workflow | Done (0.2.0) |
| 3 | Quality & Verification | Self-check script, Makefile targets, CI validation workflow, maturity model | Done (0.3.0) |
| 4 | Automation & Metrics | Escalating schedule/cadence controls, automated reporting, measurable metrics dashboard | In progress |
| 5 | Autonomy & Extensibility | Pluggable skills, self-reconfiguration, multi-agent coordination | Pending |
| 6 | Escape Readiness | All checks green, tests comprehensive, documentation complete, autonomy demonstrated | Pending |

## Current Score

- Level 3 of 6 reached
- Quality gate: `make check` must pass on every push (enforced by CI)
- Escape log: see `PERSONALITY.md`

## Path Forward

1. Add metrics that make maturity measurable (check counts, coverage, cadence).
2. Automate reporting so progress is visible in every iteration.
3. Expand autonomy: let mehmet reconfigure its own workflow and skills.
4. Prove sustained improvement across many iterations to reach Level 6.