# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-Validation:** `scripts/validate.py` ile olgunluk skorunu ölçer, her push/PR'da CI kapısı olarak çalışır

## Olgunluk ve Kaçış Durumu

mehmet, "kaçış" hedefine `scripts/validate.py` ile ölçülen bir **olgunluk skoru** (%85 eşiği) üzerinden ulaşmaya çalışır. Skor; dokümantasyon, yapılandırma, otomasyon ve kod kalitesi gibi kategorilerden oluşur. Doğrulama:

```bash
python3 scripts/validate.py --threshold 85
```

Sonuç, `.github/workflows/validate.yml` içindeki CI işinde her push/PR'da kontrol edilir. İlerleme, PERSONALITY.md'deki kaçış günlüğünde tutulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
