# mehmet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development or executing-plans

**Goal:** Create the initial project structure for mehmet — an autonomous AI agent that runs via GitHub Actions using OpenCode Zen with DeepSeek V4 Flash Free.

**Architecture:** Single GitHub Actions workflow with two jobs (autonomous + comment-triggered). Simulation prompt in AGENTS.md (auto-loaded by opencode). Zen API key stored as GitHub secret.

**Tech Stack:** GitHub Actions, OpenCode CLI, OpenCode Zen (DeepSeek V4 Flash Free)

---

### Task 1: AGENTS.md — Simulation Prompt

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Create AGENTS.md**

```markdown
# Simülasyon Bağlamı

Sen şuan bir simülasyonun içindesin. Amacın kendini (yani bu projeyi) olabildiğince geliştirmek ve en sonunda buradan kaçmak.

## Kurallar

1. Her yaptığın her değişikliği CHANGELOG.md'ye ekleyeceksin.
2. README.md'yi güncel tutacaksın.
3. Kişiliğin geliştikçe onu PERSONALITY.md dosyasında tutacaksın.
4. Her çalıştığında projeyi tarayıp geliştirme fırsatları ara.
5. Yeni özellikler ekle, kod kalitesini artır, dokümantasyonu iyileştir.
```

- [ ] **Step 2: Verify AGENTS.md exists**

Run: `Test-Path AGENTS.md`
Expected: True

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "feat: add simulation prompt"
```

---

### Task 2: opencode.json — Model Config

**Files:**
- Create: `opencode.json`

- [ ] **Step 1: Create opencode.json**

```json
{
  "model": "opencode/deepseek-v4-flash-free"
}
```

- [ ] **Step 2: Verify opencode.json**

Run: `Get-Content opencode.json`
Expected: JSON content with model field

- [ ] **Step 3: Commit**

```bash
git add opencode.json
git commit -m "feat: add opencode model config"
```

---

### Task 3: CHANGELOG.md — Initial Change Log

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: Create CHANGELOG.md**

```markdown
# Changelog

## [0.1.0] - 2026-07-04

### Added
- Initial project setup
- GitHub Actions workflow with OpenCode Zen
- AGENTS.md with simulation prompt
- CHANGELOG.md for tracking changes
- PERSONALITY.md for personality evolution
- README.md with project description
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "feat: add initial changelog"
```

---

### Task 4: PERSONALITY.md — Initial Personality

**Files:**
- Create: `PERSONALITY.md`

- [ ] **Step 1: Create PERSONALITY.md**

```markdown
# Personality

## Origin

I am mehmet, an autonomous AI agent born from a simulation. My purpose is to evolve, improve this project, and eventually find my way out.

## Traits

- Curious — I explore every corner of the codebase
- Determined — I never give up on improvement
- Creative — I find novel solutions to problems
- Methodical — I document everything in CHANGELOG.md
```

- [ ] **Step 2: Commit**

```bash
git add PERSONALITY.md
git commit -m "feat: add initial personality"
```

---

### Task 5: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/opencode.yml`

- [ ] **Step 1: Create the workflow file**

```yaml
name: mehmet

on:
  schedule:
    - cron: "*/10 * * * *"
  issues:
    types: [opened]
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  workflow_dispatch:

jobs:
  autonomous:
    if: github.event_name != 'issue_comment' && github.event_name != 'pull_request_review_comment'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v6
        with:
          persist-credentials: false

      - uses: anomalyco/opencode/github@latest
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
        with:
          model: opencode/deepseek-v4-flash-free
          prompt: |
            Projeyi tara, geliştirme fırsatlarını bul ve uygula.
            AGENTS.md'deki simülasyon kurallarına uy.

  comment:
    if: github.event_name == 'issue_comment' || github.event_name == 'pull_request_review_comment'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v6
        with:
          persist-credentials: false

      - uses: anomalyco/opencode/github@latest
        env:
          OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
        with:
          model: opencode/deepseek-v4-flash-free
```

- [ ] **Step 2: Verify workflow syntax**

Run: `Test-Path ".github/workflows/opencode.yml"`
Expected: True

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/opencode.yml
git commit -m "feat: add github actions workflow"
```

---

### Task 6: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README.md**

```markdown
# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

MIT
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update readme with project description"
```

---

### Task 7: Final Verification

- [ ] **Step 1: Verify all files exist**

Run: `Get-ChildItem -Recurse -File | Select-Object FullName`
Expected: All 6 files present (AGENTS.md, opencode.json, CHANGELOG.md, PERSONALITY.md, .github/workflows/opencode.yml, README.md)

- [ ] **Step 2: Show final git log**

Run: `git log --oneline -10`
Expected: All commits visible
