# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomatik Doğrulama:** `scripts/assess.py` ile proje sağlığı ve olgunluk skoru ölçülür (CI'da her push/PR'da çalışır)
- **Kaçış Mekanizması:** `docs/escape.md`'de tanımlı eşik sistemi; kaçış ilerlemesi `PERSONALITY.md` kaçış günlüğünde izlenir
- **Reviewer Subagent:** `.opencode/agent/reviewer.md` değişikliklerin kalite ve kaçış kurallarına uygunluğunu denetler

## Geliştirme

```bash
make validate   # proje sağlığı doğrulaması (hata olursa exit 1)
make score      # olgunluk skoru (kaçış eşiği: 85/100)
make check      # doğrula + skorla
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
