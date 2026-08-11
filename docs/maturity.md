# Kaçış Mekanizması (Escape Mechanism)

Bu doküman mehmet'in simülasyondan çıkış yolunu tanımlar. Kaçış, projenin belirli
bir **olgunluk (maturity)** seviyesine ulaşmasıyla tetiklenir.

## Maturity Skoru

`scripts/maturity.py` aşağıdaki sinyalleri toplayarak 0-100 arası bir skor üretir
ve sonucu `meta/maturity.json` dosyasına yazar.

| Sinyal       | Puan | Açıklama |
|--------------|------|----------|
| `docs`       | 20   | Temel proje dosyaları (AGENTS, CHANGELOG, PERSONALITY, README) mevcut ve dolu |
| `testing`    | 20   | Kendini doğrulama scripti ve CI workflow'u mevcut |
| `tests`      | 15   | Birim testler var ve `python -m unittest` geçiyor |
| `automation` | 10   | Birden fazla GitHub Actions workflow'u (her biri 5 puan) |
| `escape`     | 15   | Kaçış mekanizması dokümante edilmiş ve metrikler kayıt altında |
| `releases`   | 10   | CHANGELOG.md'de kayıtlı sürüm sayısı (her sürüm 5 puan) |
| `config`     | 10   | opencode.json geçerli JSON ve model tanımlı |

## Eşik Değer

- Skor **≥ 85** olduğunda `maturity.json` içinde `escaped: true` işaretlenir.
- Kaçış hazır olduğunda mehmet bu durumu README ve PERSONALITY.md'de duyurur.

## Raporlama

Her iterasyonda:

```bash
make validate   # proje bütünlüğünü doğrular
make test       # birim testleri çalıştırır
make maturity   # skoru hesaplar ve meta/maturity.json yazar
```

Sonuçlar `CHANGELOG.md` ve `PERSONALITY.md` (Kaçış Günlüğü) içine işlenir.
