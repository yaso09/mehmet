# mehmet Iteration 3 — Maturity & Validation Infrastructure

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development or executing-plans

**Goal:** Add concrete escape infrastructure to mehmet: automated health validation (test altyapısı), CI enforcement, and a machine-checkable maturity model with a score (maturity threshold from AGENTS.md rule 6 & the design spec's "Gelecek Geliştirmeler").

**Architecture:** Two bash scripts under `scripts/` (validate.sh, maturity.sh), one new CI workflow (`ci.yml`), a maturity model doc (`docs/maturity.md`), and hardening of the autonomous workflow (`timeout-minutes`).

**Tech Stack:** Bash, GitHub Actions, yamllint / jq / PyYAML (validation tooling).

---

### Task 1: `scripts/validate.sh` — Project Health Validation

**Files:**
- Create: `scripts/validate.sh`

- [x] Validates JSON (`opencode.json`), YAML workflows, and presence/format of core artifacts (AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md, LICENSE)
- [x] Exits non-zero on any failure for CI use
- [x] Verify: `bash scripts/validate.sh` → 10/10 pass, exit 0

---

### Task 2: `.github/workflows/ci.yml` — CI Enforcement

**Files:**
- Create: `.github/workflows/ci.yml`

- [x] Runs `scripts/validate.sh` on pushes to `main` and all PRs
- [x] `concurrency` group + `timeout-minutes: 10`
- [x] Verify: `yamllint` clean; validated by `scripts/validate.sh`

---

### Task 3: `docs/maturity.md` — Maturity Model / Escape Criteria

**Files:**
- Create: `docs/maturity.md`

- [x] Defines 23 machine-checkable criteria across 4 categories (Test Altyapısı, Kod Kalitesi, Dokümantasyon, Otomasyon)
- [x] Defines maturity levels and the escape threshold (score ≥ 90 + green CI)
- [x] Documents the escape protocol

---

### Task 4: `scripts/maturity.sh` — Maturity Score

**Files:**
- Create: `scripts/maturity.sh`

- [x] Evaluates all 23 criteria, prints per-criterion PASS/FAIL + score + level
- [x] Recursion guard (`MATURITY_GUARD=1`) so TC-05 self-check terminates
- [x] Verify: `bash scripts/maturity.sh` → score/level normal, exits accordingly

---

### Task 5: Harden `opencode.yml`

**Files:**
- Modify: `.github/workflows/opencode.yml`

- [x] Add `timeout-minutes: 30` to both `autonomous` and `comment` jobs
- [x] Verify: yamllint clean

---

### Task 6: Update CHANGELOG.md / README.md / PERSONALITY.md

- [x] CHANGELOG.md: add `[0.3.0]` entry (fixes QC-05, 3+ version entries)
- [x] README.md: document validation/maturity tooling
- [x] PERSONALITY.md: evolve personality, append escape-log row

---

### Task 7: Final Verification

- [x] `bash scripts/validate.sh` → all pass, exit 0
- [x] `bash scripts/maturity.sh` → score 100/100 (Escape) recorded
- [x] `yamllint` clean on all workflows
- [x] Commit all changes