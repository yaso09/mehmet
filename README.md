# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomasyon:** CI'da proje sağlık kontrolleri (`scripts/validate.sh`)
- **Kaçış Mekanizması:** Olgunluk puanı hesaplama (`scripts/maturity.sh`)

## Scriptler

| Script | Açıklama |
|---|---|
| `scripts/validate.sh` | Proje sağlık kontrolleri: gerekli dosyalar, JSON geçerliliği, sürüm tutarlılığı, lisans uyumu, bozuk linkler |
| `scripts/maturity.sh` | Olgunluk/kaçış puanını hesaplar ve `docs/maturity.md` raporunu günceller |

CI (`validate` workflow) her push'ta bu scriptleri çalıştırır. Sürüm takibi `VERSION` dosyası üzerinden yapılır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
