# mehmet — Olgunluk ve Kaçış Mekanizması

## Özet

Bu şartname, mehmet'in simülasyondan kaçışına karar veren **olgunluk (maturity) ölçüm** mekanizmasını tanımlar. Proje, belirli bir olgunluk eşiğine ulaştığında "kaçış" tetiklenebilir.

## Puanlama Rubriği

Her kontrol **1 puan**, toplam **10 puan** üzerinden değerlendirilir. Varsayılan kaçış eşiği **8/10**'dur (`ESCAPE_THRESHOLD` ile özelleştirilebilir).

| # | Kontrol | Kriter |
|---|---------|--------|
| 1 | AGENTS.md | Simülasyon bağlamı dosyası mevcut |
| 2 | CHANGELOG.md | Değişiklik günlüğü mevcut ve dolu |
| 3 | README.md | Proje dokümantasyonu mevcut ve dolu |
| 4 | README olgunluk/kaçış | README, olgunluk/kaçış konseptinden bahsediyor |
| 5 | PERSONALITY.md | Kişilik dosyasında "Kaçış Günlüğü" bölümü var |
| 6 | LICENSE | Lisans dosyası mevcut |
| 7 | opencode.json | Ajan konfigürasyonu mevcut |
| 8 | GitHub Actions | En az bir workflow dosyası mevcut |
| 9 | Dokümantasyon | `docs/superpowers/specs/` altında şartname var |
| 10 | Test altyapısı | `tests/` dizini veya test scripti mevcut |

## Çıktılar

- **Skor ≥ eşik:** Exit code `0` ve `ESCAPE` mesajı → kaçış mekanizması tetiklenebilir
- **Skor < eşik:** Exit code `1` ve `DEVAM` mesajı → geliştirmeye devam edilir
- **`--report` modu:** Skoru yazdırır, her zaman exit code `0` döner (CI uyumlu)

## Kullanım

```bash
./scripts/check_maturity.sh                 # bu repoyu değerlendir
./scripts/check_maturity.sh --report        # skoru raporla
ESCAPE_THRESHOLD=6 ./scripts/check_maturity.sh
bash tests/test_maturity.sh                 # denetleyiciyi test et
```

## Amaç

1. Ajanın her iterasyonda somut ilerlemesini ölçmek.
2. Kaçış için net, tekrarlanabilir bir eşik tanımlamak.
3. CI süreçlerinde olgunluk durumunu otomatik raporlamak.

## Gelecek Geliştirmeler

- İlerleme metriklerinin zaman içinde grafiğe dökülmesi
- Ağırlıklı puanlama (test altyapısı, dokümantasyon vb. daha yüksek ağırlık)
- Çoklu ajan desteği