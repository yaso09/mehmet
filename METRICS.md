# Maturity Score

The escape mechanism is driven by a measurable maturity score computed by `scripts/score.mjs`.

## Scorecard

| Dimension     | Weight | Pass |
|---------------|--------|------|
| README        | 10     | yes  |
| CHANGELOG     | 10     | yes  |
| PERSONALITY   | 10     | yes  |
| AGENTS        | 10     | yes  |
| Tests         | 15     | yes  |
| CI            | 15     | yes  |
| Config        | 10     | yes  |
| Workflow      | 10     | yes  |
| License       | 10     | yes  |

**Current score: 100/100**

**Escape threshold: 80/100** — reached when the project sustains all checks above the threshold.

## History

| Iteration | Score | Note |
|-----------|-------|------|
| 1         | 50/100 | Initial structure only |
| 2         | 60/100 | Config, gitignore, workflow hardening |
| 3         | 100/100 | Tests, CI, maturity scoring added |