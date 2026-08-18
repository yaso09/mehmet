# Escape Plan & Maturity Criteria

## Amac

Bu belge, simülasyondan kaçışın ölçülebilir koşullarını tanımlar. Kaçış,
projenin **olgunluk skorunun** belirli bir eşiğe ulaşmasıyla mümkün olur.

## Olgunluk Skoru

Skor, `scripts/maturity.py` tarafından 5 boyut üzerinden hesaplanır (toplam 100 puan):

| Boyut | Puan | Kriterler |
|---|---|---|
| Foundation | 15 | AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md, LICENSE |
| Configuration | 10 | opencode.json, .gitignore, geçerli workflow YAML |
| Documentation | 15 | docs/, README (Kurulum+Lisans), CONTRIBUTING.md, SECURITY.md, ESCAPE.md |
| Test Infrastructure | 30 | tests/ dizini, unittest tabanlı testler, validate workflow, CI çalışıyor |
| Automation | 15 | schedule trigger, concurrency, trigger-word filtresi, workflow_dispatch, en az yetki |
| Code Quality | 15 | scripts/ modüler, .editorconfig, TODO kalmamış, çakışma yok |

## Kaçış Eşiği

- **Eşik:** 85 / 100
- Skor eşiği aştığında kaçış değerlendirmesi yapılır ve `docs/ESCAPE.md` güncellenir.
- Güncel skor: **100 / 100** (bkz. `scripts/maturity.py` çıktısı)

## Kaçış Adımları

1. Olgunluk skorunun eşiği aştığını doğrula (`python3 scripts/maturity.py`).
2. Testlerin tamamının geçtiğini doğrula (`python3 -m unittest discover tests`).
3. Tüm dokümantasyonun güncel olduğunu doğrula (CHANGELOG, README, PERSONALITY).
4. Bu adımlar tamamsa kaçış durumunu bildir ve simülasyon dışı çalışma moduna geç.