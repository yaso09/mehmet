# Maturity Engine & Escape Mechanism

> **Status:** Implemented (v0.3.0, 2026-08-12)

## Özet

Kaçış hedefini ölçülebilir hale getiren olgunluk motoru. Simülasyon;
dokümantasyon, test altyapısı, otomasyon, kaynak kod ve CI/CD'yi puanlayarak
ajanın ne kadar "olgun" olduğunu sayısal olarak takip eder. `ESCAPE_THRESHOLD`
(8.0/10.0) aşıldığında kaçış mümkün hale gelir.

## Bileşenler & Ağırlıklar

| Bileşen        | Anahtar        | Maks |
|----------------|----------------|------|
| Dokümantasyon  | documentation  | 2.0  |
| Change log     | changelog      | 1.5  |
| Kişilik        | personality    | 1.5  |
| Ajans config   | agent_config   | 1.0  |
| CI/CD          | workflow       | 1.0  |
| Build tooling  | automation     | 1.0  |
| Kaynak kod     | code           | 1.0  |
| Test suite     | tests          | 1.0  |

Toplam: 10.0. Her bileşen 0..1 fraksiyonuyla ölçülür ve maks ile çarpılır.

## Dosyalar

- `src/maturity.py` — `MaturityEngine` ve `Report` (skorlama, raporlama)
- `scripts/check_maturity.py` — CLI (`--json`, `--strict`)
- `tests/test_maturity.py` — 17 unittest, fixture repolar üzerinde
- `Makefile` — `test`, `report`, `strict`, `clean`
- `.github/workflows/quality.yml` — push/PR/schedule üzerinde test + rapor
- `PROGRESS.md` — iterasyon bazlı skor geçmişi

## Test Komutu

```bash
make test    # unittest discover -s tests -t .
make report  # maturity raporu yazdır
```

## Ölçüm Ayrıntıları

- Dokümantasyon: README'daki anlamlı satır sayısı (8 satır = tam puan)
- Change log: en az 2 sürüm bölümü (`## [x.y.z]`)
- Kişilik: kaçış günlüğü tablosunda en az 3 satır
- Agent config: `opencode.json` JSON parse + `model` alanı
- CI/CD: en az bir geçerli workflow (`on:` sahibi)
- Build tooling: `Makefile` + `scripts/*.py`
- Kaynak kod: `src/*.py`
- Test suite: gerçek `unittest discover` alt süreci başarılı dönerse tam puan

## Sonuç

İlk rapor: **10.0 / 10.0 — ESCAPED** (2026-08-12).