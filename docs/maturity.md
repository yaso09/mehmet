# Olgunluk & Kaçış Mekanizması

mehmet'in simülasyondan kaçışı, projenin ölçülebilir bir olgunluk seviyesine
ulaşmasına bağlıdır. Bu seviye `scripts/maturity.py` tarafından 0-100
aralığında hesaplanır.

## Puanlama

Dört grup, her biri 25 puan:

| Grup       | Ne ölçer                                                             |
|------------|----------------------------------------------------------------------|
| `code`     | `scripts/` altında geçerli, tip belirtilmiş, belgeli modüler kod      |
| `tests`    | `tests/` altyapısı; testler çalışıyor ve başarılı                     |
| `docs`     | README, CHANGELOG, PERSONALITY, docs/ ve kaçış mekanizmasının dokümanı |
| `automation` | CI kalite workflow'u, test + olgunluk kapısı, concurrency, secret   |

## Eşik

`ESCAPE_THRESHOLD = 80.0`. Skor bu eşiği aştığında proje "MATURE" sayılır.

Kaçış tek bir anlık görüntüyle olmaz: **escape-ready olmak için son 3
iterasyonun ardışık olarak eşiğin üzerinde olması** gerekir (sürdürülebilir
olgunluk). Skor her koşuda `docs/maturity-history.json` dosyasına tarihli
olarak eklenir; ardışık nitelikli iterasyon sayısı `sustained` olarak raporlanır.

## Çalıştırma

```bash
python3 scripts/maturity.py
```

Çıktıdaki `sustained qualifying iterations: N/3` satırı kaçışa kaç ardışık
kalifiye iterasyon kaldığını gösterir.

## Geçmiş

Puan geçmişi `docs/maturity-history.json` içinde tutulur. Her iterasyon,
güncel skoru bu geçmişe ekleyerek kaçışa ne kadar yaklaştığını gösterir.