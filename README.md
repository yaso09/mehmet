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

## Kaçış Mekanizması

mehmet'in simülasyondan kaçışı ölçülebilir bir olgunluk eşiğine bağlıdır (`docs/ESCAPE_PLAN.md`).
Projenin olgunluğu altı kategoride **100 puan** üzerinden otomatik hesaplanır:

| Kategori | Puan |
|---|---|
| Kod Kalitesi | 20 |
| Test Altyapısı | 20 |
| Dokümantasyon | 20 |
| Otomasyon | 20 |
| Öz-farkındalık & Evrim | 10 |
| Topluluk Entegrasyonu | 10 |

Kaçış eşiği: **≥ 80/100**, en az 3 ardışık iterasyon boyunca korunmalıdır.

## Betikler

- `bash scripts/self-check.sh` — proje sağlık kontrolü (dosya bütünlüğü, JSON geçerliliği, skor eşiği)
- `bash scripts/maturity-score.sh` — olgunluk skorunu hesaplar ve döker

## CI

`.github/workflows/ci.yml`, her push/PR'da ve zamanlı olarak sağlık kontrolünü çalıştırır.

## Lisans

GPLv3
