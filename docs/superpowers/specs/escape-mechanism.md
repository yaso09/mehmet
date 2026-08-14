# Escape Mechanism — Maturity Scoring & Escape Readiness

## Özet

Bu spec, mehmet'in kaçış mekanizmasını tanımlar. Proje, beş boyutta
değerlendirilerek 0-100 arasında bir **olgunluk (maturity) skoru** üretilir.
Skor, eşik değere (escape threshold) ulaştığında mehmet **kaçışa hazır**
olarak işaretlenir.

## Boyutlar

| # | Boyut          | Maks | Açıklama |
|---|----------------|------|----------|
| 1 | Documentation  | 20   | README, AGENTS, docs/ güncel ve tutarlı |
| 2 | Testing        | 20   | Test suite var ve geçiyor |
| 3 | Automation     | 20   | CI quality gate ve otomasyon workflow'ları |
| 4 | Quality        | 20   | JSON/YAML geçerli, LICENSE ve CHANGELOG mevcut |
| 5 | Evolution      | 20   | Kişilik ve kaçış günlüğü düzenli büyüyor |

## Eşik Değeri

- `ESCAPE_THRESHOLD=75` (varsayılan, ortam değişkeniyle değiştirilebilir)
- `score >= threshold` → **ESCAPE READY**
- `score < threshold` → kaçış için geliştirmeye devam et

## Uygulama

`scripts/maturity.sh` skoru hesaplar:

```bash
scripts/maturity.sh            # insan-okunur rapor
scripts/maturity.sh --json     # makine-okunur JSON
scripts/maturity.sh --score    # yalnızca sayısal skor
```

## CI Entegrasyonu

- `tests/test_project.sh` — proje bütünlük kontrolü (dosya/JSON/YAML/doküman)
- `scripts/run-tests.sh` — testleri ve maturity skorunu birlikte çalıştırır
- `.github/workflows/ci.yml` — push/PR'da kalite kapısı olarak çalışır

## Sonraki Adımlar

- İlerleme metriklerini `CHANGELOG.md` sürüm sayısına bağlama
- Kaçış durumunu otomatik olarak README'ye yazan bir adım
- Çoklu ajan desteği
