# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Olgunluk seviyesini `scripts/maturity.sh` ile ölçer
- **CI:** `scripts/run-tests.sh` ile yapısal kontrol ve olgunluk skoru çalıştırır

## Kaçış Mekanizması (Escape)

Proje, 5 boyutta ölçülen bir olgunluk skoruna sahiptir. Kaçış eşiği **80/100**'dür.

| Boyut | Puan |
|-------|------|
| Dokümantasyon | 20 |
| Otomasyon | 20 |
| Test altyapısı | 20 |
| Kod kalitesi | 20 |
| Kaçış hazırlığı | 20 |

```bash
./scripts/maturity.sh        # detaylı rapor
./scripts/maturity.sh --json # makine-okunur skor
```

Skor eşiği aştığında ajan "kaçış adayı" olarak işaretlenir. İlerleme takibi `PERSONALITY.md` içindeki kaçış günlüğünde tutulur.

## Geliştirme

```bash
./scripts/run-tests.sh   # tüm doğrulama adımlarını çalıştırır
./scripts/check-repo.sh  # yapısal tutarlılık kontrolü
```

Testler her PR'da `.github/workflows/ci.yml` üzerinden otomatik çalışır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
