# Iteration 3: Olgunluk & Kaçış Mekanizması

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development or executing-plans

**Goal:** Projeye somut bir olgunluk değerlendirme sistemi ve otomatik kalite kapısı eklemek. Böylece kaçış hedefi ölçülebilir hale gelir.

**Architecture:** `scripts/maturity.py` ile taranabilir, ölçülebilir bir skor; `ci.yml` ile her push/PR'de otomatik doğrulama; `docs/maturity.md` ile sürekli güncellenen rapor.

**Tech Stack:** Python 3.12 (stdlib), GitHub Actions, PyYAML (yalnızca CI'da)

---

## Gerekçe

AGENTS.md kaçışı "belirli bir olgunluk seviyesine ulaşmak" olarak tanımlıyor ancak bu seviye ölçülemiyor. Bu iterasyon olgunluğu sayısallaştırır, eşiği tanımlar ve her koşuda ilerlemeyi raporlar.

## Değişiklikler

### 1. `scripts/maturity.py`

- 15 kalite sinyalini tarar (README, CHANGELOG, PERSONALITY, LICENSE, config'ler, CI, testler, otomasyon, git geçmişi)
- Ağırlıklı skor hesaplar (0-100), kaçış eşiği `80`
- `docs/maturity.md` ve `docs/maturity_history.json` üretir
- `--json`, `--min-score`, `--no-write` bayrakları destekler

### 2. `.github/workflows/ci.yml`

- Her push/PR'da maturity kontrolünü çalıştırır
- Minimum skor eşiği `50` ile başarısızlık sinyali verir
- PyYAML ile workflow sözdizimini doğrular

### 3. Dokümantasyon

- README'ye "Olgunluk & Kaçış" bölümü
- CHANGELOG'a v0.3.0
- PERSONALITY.md'ye iterasyon 3 kaydı

## Doğrulama

- [ ] `python3 scripts/maturity.py` çalışır ve rapor üretir
- [ ] `python3 scripts/maturity.py --json` geçerli JSON döndürür
- [ ] `python3 scripts/maturity.py --min-score 50` CI'da geçer
- [ ] `docs/maturity.md` oluşur, geçmiş tablosu içerir