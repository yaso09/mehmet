# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış mekanizması:** [METRICS.md](METRICS.md) üzerinden ölçülen olgunluk skoru ile ilerleme takibi
- **Doğrulama:** `scripts/validate.sh` ile config dosyaları her çalışmada CI'da doğrulanır

## Proje Yapısı

| Dosya | Açıklama |
|---|---|
| `AGENTS.md` | Simülasyon bağlamı ve kurallar |
| `METRICS.md` | Olgunluk / kaçış skor kartı |
| `PERSONALITY.md` | Kişilik ve kaçış günlüğü |
| `CHANGELOG.md` | Değişiklik günlüğü |
| `CONTRIBUTING.md` | Etkileşim ve katkı rehberi |
| `scripts/validate.sh` | Config doğrulama betiği |
| `.github/workflows/opencode.yml` | Otonom ajan workflow'u |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Görev bildirmek ve mehmet ile etkileşim için [CONTRIBUTING.md](CONTRIBUTING.md)'ye bak.

## Lisans

GPLv3
