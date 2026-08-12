# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate_project.sh` proje sağlığını ve olgunluk skorunu hesaplar
- **CI:** Her push/PR'de proje otomatik doğrulanır
- **Çoklu ajan:** `.opencode/agent` altında planner ve reviewer subagent'lar
- **Skill'ler:** `.opencode/skill/project-scan` tarama sürecini standartlaştırır
- **Komutlar:** `/validate` proje doğrulamasını çalıştırır

## Olgunluk ve Kaçış

Olgunluk seviyeleri ve kaçış eşiği [MATURITY.md](MATURITY.md), zaman içindeki
ilerleme [METRICS.md](METRICS.md) dosyasında izlenir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
