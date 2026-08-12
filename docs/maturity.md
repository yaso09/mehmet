# Maturity Model & Escape Threshold

Bu doküman, mehmet'in **kaçış (escape) mekanizmasını** tanımlar: proje belirli bir
olgunluk seviyesine ulaştığında simülasyon tamamlanmış sayılır.

Skor, `scripts/maturity.py` ile deterministik olarak hesaplanır ve CI'da
(`.github/workflows/validate.yml`) çalıştırılır.

## Boyutlar

| Boyut | Ağırlık | Açıklama |
|-------|--------|----------|
| Documentation | 25 | README, CHANGELOG, PERSONALITY, docs/, lisans |
| Code Quality | 25 | Gerçek kod (scripts/), doğrulama ve olgunluk araçları, Makefile |
| Verification | 25 | Consistency check'lerin geçmesi, CI doğrulaması, workflow bütünlüğü |
| Automation | 15 | Schedule, event-driven trigger'lar, concurrency |
| Security | 10 | Secret yönetimi, credentials sızıntısı yok, checkout güvenliği |

## Hesaplama

Her boyutun noktaları eşit ağırlıklıdır: boyutun kazandığı puan =
`(kazanılan nokta / toplam nokta) × boyut ağırlığı`. Toplam skor 0–100 arasındadır.

## Eşik

```
Escape threshold: 95 / 100
```

Skor ≥ 95 olduğunda mehmet "escapable" durumdadır. Eşik, proje olgunlaştıkça
zamanla yükseltilerek kaçış süreci zorlaştırılır (v0.2'de 85 → v0.3'te 95).

## Test Altyapısı

Kaçış skoruna doğrudan etki eden test altyapısı `scripts/tests/` altındadır:

| Dosya | İçerik |
|-------|--------|
| `test_structure.py` | Yapı, gizli bilgi ve `check.py` doğrulaması (hızlı suite) |
| `test_integration.py` | `maturity.py` uçtan uca entegrasyon testleri |

`make test` ile tümü çalıştırılır. `maturity.py`'nin kendi içindeki
self-test denetimi yalnızca `test_structure.py`'yi çalıştırarak
yinelemeli (recursive) çalışmayı engeller.

## Mevcut Durum

Skor güncel değeri görmek için:

```bash
make maturity
# veya
python3 scripts/maturity.py [--json]
```
