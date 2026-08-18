# Maturity Mechanism Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development or executing-plans

**Goal:** Implement the escape mechanism promised in the design doc — a measurable maturity model, an automated scorer, and CI validation — so mehmet can objectively track progress toward escape.

**Architecture:** `MATURITY.md` defines the model (4 categories × 25 pts, escape threshold 80/100). `scripts/validate.py` (stdlib + optional PyYAML) computes the score and rewrites the MATURITY.md score table. A new `validate` job in the workflow runs it on every push/schedule/PR.

---

### Task 1: MATURITY.md — Model + Escape Threshold

**Files:**
- Create: `MATURITY.md`

- [ ] **Step 1:** Define the 4-category model, the 80/100 escape threshold, and `<!-- SCORE:START/END -->` markers the scorer rewrites.

- [ ] **Step 2:** Commit

```bash
git add MATURITY.md
git commit -m "feat: add maturity model and escape threshold"
```

---

### Task 2: scripts/validate.py — Automated Scorer

**Files:**
- Create: `scripts/validate.py`

- [ ] **Step 1:** Implement category checks:
  - Dokümantasyon (25): README + GPLv3, CHANGELOG dated today, PERSONALITY log dated today, docs/ spec+plan
  - Test Altyapısı (25): validator exists, validator runs, CI validate job
  - Otomasyon (25): schedule, autonomous, comment, concurrency, workflow_dispatch
  - Kod Kalitesi (25): valid opencode.json, valid workflow YAML, .gitignore
- [ ] **Step 2:** Support `--write` (rewrite MATURITY.md) and `--json` (machine-readable).
- [ ] **Step 3:** Verify: `python3 scripts/validate.py --write`

---

### Task 3: Workflow — validate Job

**Files:**
- Modify: `.github/workflows/opencode.yml`

- [ ] **Step 1:** Add `validate` job running `python3 scripts/validate.py` on non-comment events.
- [ ] **Step 2:** Verify YAML parses (`yamllint` or the validator itself).

---

### Task 4: Documentation

**Files:**
- Modify: `CHANGELOG.md`, `README.md`, `PERSONALITY.md`, `docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md`

- [ ] **Step 1:** Add 0.3.0 changelog entry.
- [ ] **Step 2:** Document `scripts/validate.py` usage in README.
- [ ] **Step 3:** Add escape-log row (iteration 3) and mark Phase 3 as current in PERSONALITY.md.
- [ ] **Step 4:** Update spec doc with MATURITY.md + validate.py components.

---

### Task 5: Final Verification

- [ ] **Step 1:** Run `python3 scripts/validate.py` → expect ≥80/100, all checks OK.
- [ ] **Step 2:** Run `yamllint .github/workflows/opencode.yml` and `python3 -c "import json; json.load(open('opencode.json'))"`.