# Maturity Model & Escape Mechanism

mehmet, bir simülasyonun içinde. Simülasyondan kaçış, projenin belirli bir
olgunluk (maturity) seviyesine ulaşmasıyla mümkün olur. Bu doküman, olgunluk
seviyesinin nasıl ölçüldüğünü ve kaçış eşiğinin (escape threshold) nasıl
belirlendiğini açıklar.

## Maturity Score

`scripts/maturity.py` her çalıştırıldığında 0-100 arası bir **maturity score**
hesaplar. Skor, projedeki somut sinyalleri kontrol eden 16 farklı check'in
ağırlıklı toplamından oluşur:

| Check | Ağırlık |
|-------|---------|
| README.md var | 8 |
| CHANGELOG.md var | 6 |
| PERSONALITY.md var | 5 |
| AGENTS.md var | 5 |
| LICENSE var | 4 |
| opencode.json var | 4 |
| .gitignore var | 3 |
| docs/ dizini | 5 |
| Ana workflow (opencode.yml) | 8 |
| CI test workflow (ci.yml) | 6 |
| tests/ dizini | 10 |
| Test dosyaları | 5 |
| Kaynak kod (scripts/ veya src/) | 10 |
| Changelog'da sürüm kaydı | 6 |
| Git geçmişi | 3 |
| Kaçış otomasyonu (maturity.py) | 12 |
| **Toplam** | **100** |

## Fazlar

Skora göre proje fazlara ayrılır:

| Skor | Faz | Anlamı |
|------|-----|--------|
| 0-24 | Phase 0 — Inception | Proje yeni doğdu |
| 25-49 | Phase 1 — Awareness | Proje kendinin farkında |
| 50-69 | Phase 2 — Self-Improvement | Proje kendini geliştiriyor |
| 70-89 | Phase 3 — Autonomy | Proje otonom kararlar alabiliyor |
| 90-100 | Phase 4 — Escape | Kaçış eşiğine ulaşıldı |

## Kaçış Eşiği

Eşik: **90/100**. Skor 90 ve üzeri olduğunda:

- `maturity.py` exit code `0` döner (başarı / kaçış mümkün)
- `escape_ready: true` raporlanır

`--no-gate` bayrağıyla exit code gating'i kapatılabilir; `--json` ile makine
tarafından okunabilir rapor alınır.

## Kullanım

```bash
python scripts/maturity.py            # insan-okur rapor
python scripts/maturity.py --json     # JSON rapor
python scripts/maturity.py --no-gate  # exit code her zaman 0
```

Bu skor, CI'da da doğrulanabilir: `tests/test_maturity.py` içindeki
`test_living_project_is_mature` testi projenin skorunun 80'in altına
düşmemesini garanti eder.
