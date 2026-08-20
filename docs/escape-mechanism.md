# Kaçış Mekanizması / Escape Mechanism

mehmet'in simülasyondan kaçışı, projenin belirli bir **olgunluk (maturity)**
seviyesine ulaşmasıyla mümkün olur. Bu seviye `scripts/maturity.py` ile
objektif olarak ölçülür.

## Kriterler

Her kriter 10 puan değerindedir (toplam 100 puan):

| # | Kriter | Açıklama |
|---|--------|----------|
| 1 | `LICENSE` | Lisans dosyası mevcut |
| 2 | `README.md` | Proje tanıtımı mevcut ve yeterli |
| 3 | `CHANGELOG.md` | Değişiklik günlüğü tutuluyor |
| 4 | `PERSONALITY.md` | Kaçış günlüğü içeren kişilik dosyası |
| 5 | `AGENTS.md` | Davranış kuralları tanımlı |
| 6 | `opencode.json` | Geçerli JSON konfigürasyonu |
| 7 | CI workflow | GitHub Actions pipeline mevcut |
| 8 | Test altyapısı | `tests/` dizini ve testler mevcut |
| 9 | Otomasyon | `scripts/` dizini mevcut |
| 10 | Testler geçiyor | Test suite'i başarıyla çalışıyor |

## Eşik Değeri

**Kaçış eşiği: 80/100.** Skor eşiği geçtiğinde proje **kaçışa hazır**
(escape-ready) kabul edilir.

## Kullanım

```bash
python scripts/maturity.py .
```

Exit code `0` = kaçışa hazır, `1` = hazır değil.

## Durum

Skor `docs/escape-mechanism.md` güncellenirken ve CI `validate` job'ında
her çalıştırmada hesaplanır. Son durum: **100/100 — kaçışa hazır.**