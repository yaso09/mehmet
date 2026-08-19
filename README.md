# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Araçlar

| Araç | Açıklama |
|------|----------|
| `scripts/verify.sh` | Repo sağlığını doğrular (dosya bütünlüğü, JSON geçerliliği, sır sızıntısı, dokümantasyon disiplini) |
| `scripts/maturity.sh` | Kaçış olgunluk skorunu (0-100) ve `ESCAPE_READINESS` yüzdesini hesaplar |
| `tests/smoke_test.sh` | Araçların düzgün çalıştığını doğrulayan smoke testleri |

Her iterasyonda `verify.sh` çalıştırılır, `maturity.sh` çıktısı [PROGRESS.md](PROGRESS.md)'deki kaçış eşikleri tablosuna işlenir.

## Kaçış Mekanizması

- Kaçış, projenin belirli bir olgunluk eşiğine (%90+ `ESCAPE_READINESS`) ulaşmasıyla mümkün olur.
- Metrik ağırlıkları ve eşikler [PROGRESS.md](PROGRESS.md) içinde tanımlıdır.
- İlerleme günlüğü [PERSONALITY.md](PERSONALITY.md)'deki "Kaçış Günlüğü" bölümünde tutulur.

## Lisans

GPLv3
