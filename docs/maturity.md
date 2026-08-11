# Maturity Model & Escape Criteria

This document defines mehmet's maturity levels and the concrete, machine-checkable
criteria that gate escape from the simulation. `scripts/maturity.sh` evaluates
every criterion below and reports a score out of 100.

The project may attempt escape only when the maturity score reaches **90 or higher**,
with **zero failures in `scripts/validate.sh`**.

## Scoring

Each criterion is a yes/no check. The score is `(passed / total) × 100`.

| Range     | Level     | Meaning                              |
|-----------|-----------|--------------------------------------|
| 0–39      | Seedling  | Project exists, little more.         |
| 40–59     | Aware     | Self-documentation in place.         |
| 60–79     | Evolving  | Automation and quality tooling live. |
| 80–89     | Autonomous| Most checks pass; near escape.       |
| 90–100    | Escape    | Maturity threshold reached.          |

## Criteria

### Test Altyapısı (Test Infrastructure)

| ID    | Check                                                        |
|-------|--------------------------------------------------------------|
| TC-01 | `scripts/validate.sh` exists                                 |
| TC-02 | `.github/workflows/ci.yml` exists (CI validation)            |
| TC-03 | `scripts/validate.sh` currently passes                       |
| TC-04 | `scripts/maturity.sh` exists                                 |
| TC-05 | `scripts/maturity.sh` currently passes                       |

### Kod Kalitesi (Code Quality)

| ID    | Check                                                        |
|-------|--------------------------------------------------------------|
| QC-01 | `opencode.json` is valid JSON                                |
| QC-02 | Workflow YAML files are syntactically valid                  |
| QC-03 | `.gitignore` protects secrets (`.env`)                       |
| QC-04 | CHANGELOG.md uses semantic versioning (`## [x.y.z]`)         |
| QC-05 | Repository has at least 3 tagged releases / version entries  |

### Dokümantasyon (Documentation)

| ID    | Check                                                        |
|-------|--------------------------------------------------------------|
| DOC-01 | `README.md` exists                                           |
| DOC-02 | README documents setup (`## Kurulum`)                        |
| DOC-03 | README documents the license (`## Lisans`)                   |
| DOC-04 | CHANGELOG.md has a dated version header                      |
| DOC-05 | PERSONALITY.md contains the escape log table                 |
| DOC-06 | Design spec exists under `docs/superpowers/specs`            |
| DOC-07 | Implementation plan exists under `docs/superpowers/plans`    |
| DOC-08 | This maturity model exists                                   |

### Otomasyon (Automation)

| ID    | Check                                                        |
|-------|--------------------------------------------------------------|
| AUT-01 | Workflow runs on schedule (`schedule`)                       |
| AUT-02 | Workflow handles issue/PR comments (`issue_comment`)         |
| AUT-03 | Workflow has `concurrency` control                           |
| AUT-04 | Workflow jobs have `timeout-minutes` protection              |
| AUT-05 | `workflow_dispatch` manual trigger enabled                   |

## Escape Protocol

1. Compute the maturity score with `scripts/maturity.sh`.
2. Run `scripts/validate.sh` and require a clean exit.
3. Both must hold **in CI** (green `ci` workflow on the default branch).
4. When the threshold is met, append an `Escape` entry to the PERSONALITY.md
   escape log declaring readiness.
