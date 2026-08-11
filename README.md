# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** `scripts/check.sh` ile repo sağlığını ve olgunluk puanını ölçer

## Durum

- **Sürüm:** 0.3.0
- **Olgunluk:** `scripts/check.sh` çalıştırılarak ölçülür
- **CI:** `check` workflow'u her push/PR'da sağlık kontrolü yapar

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Yol Haritası

- [x] Sağlık kontrol script'i (`scripts/check.sh`)
- [x] CI (`.github/workflows/check.yml`)
- [x] Kaçış planı (`docs/escape-plan.md`)
- [ ] Test framework
- [ ] Lint/format aracı
- [ ] İlerleme metrikleri

## Lisans

GPLv3