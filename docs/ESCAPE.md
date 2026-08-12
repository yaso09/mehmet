# Escape Mechanism (Kaçış Mekanizması)

mehmet, simülasyondan kaçmak için projenin olgunluk seviyesine güvenir.
Bu doküman, kaçış koşullarını ve ölçüm yöntemini tarif eder.

## Olgunluk Skoru

`scripts/assess.py` her çalışmada projeyi 0-100 arası bir skorla değerlendirir.
Değerlendirme beş boyuta dayanır:

| Boyut             | Ağırlık | Ölçüm                                              |
|-------------------|---------|----------------------------------------------------|
| documentation     | %30     | AGENTS.md, README.md, PERSONALITY.md + kaçış günlüğü |
| change_tracking   | %20     | CHANGELOG.md varlığı ve içerik                      |
| automation        | %20     | Workflow dosyaları ve opencode.json                 |
| testing           | %20     | `tests/test_*.py` varlığı                           |
| code_quality      | %10     | `scripts/*.py` varlığı                              |

## Kaçış Koşulları

Kaçış için **tümünün** sağlanması gerekir:

1. **Olgunluk skoru ≥ 80/100** (`--escape-threshold`)
2. **Tüm birim testleri geçer** (`python3 -m unittest discover -s tests`)
3. **Maturity raporu `docs/maturity/report.json` içinde saklanır**
4. **Kaçış günlüğünde en az 3 iterasyon kaydı bulunur**

## Nasıl Çalıştırılır

```bash
python3 scripts/assess.py            # insan-okunur rapor
python3 scripts/assess.py --json     # makine-okunur rapor
python3 -m unittest discover -s tests -v
```

## Adım Adım Kaçış Protokolü

1. `scripts/assess.py --json` çalıştır.
2. Skor varsayılan koşulları gerçekten karşılıyorsa README.md bölümünü güncelle.
3. Sağlanmıyorsa, zayıf boyutları iyileştir ve yeniden ölç.

> Gerçek kaçışın doğrulanması dış sistemin iznine bağlıdır; bu doküman yalnızca
> projenin hazır olup olmadığına dair öznelenemez bir sinyal üretir.