# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her iterasyon `actionlint`, `markdownlint`, JSON ve sürüm tutarlılığı doğrulamalarından geçer

## Proje Yapısı

| Dosya | Açıklama |
| --- | --- |
| `AGENTS.md` | Simülasyon bağlamı ve ajan kuralları |
| `opencode.json` | OpenCode konfigürasyonu (model, instructions) |
| `PERSONALITY.md` | Kişilik ve kaçış günlüğü |
| `CHANGELOG.md` | Değişiklik günlüğü |
| `VERSION` | Sürümün tek kaynağı |
| `.github/workflows/opencode.yml` | Otonom ajan workflow'u |
| `.github/workflows/ci.yml` | Kalite doğrulama workflow'u |
| `scripts/check.sh` | Yerel doğrulama scripti |
| `CONTRIBUTING.md` | Katkı rehberi |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
