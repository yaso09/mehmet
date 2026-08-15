# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Yapı

- `AGENTS.md` — Simülasyon bağlamı ve kurallar
- `MATURITY.md` — Kaçış hedefi için olgunluk takibi
- `PERSONALITY.md` — Ajanın kişiliği ve kaçış günlüğü
- `CHANGELOG.md` — Değişiklik günlüğü
- `docs/superpowers/` — Tasarım ve uygulama dokümanları
- `scripts/verify-project.sh` — Proje bütünlük doğrulama scripti

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
