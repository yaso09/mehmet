# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomatik doğrulama:** Her push/PR'de `scripts/validate.py` ve testler CI'da çalışır

## Geliştirme

Proje sağlığını doğrulamak için bağımlılıksız (sadece Python stdlib) araçlar:

```bash
make validate   # proje dosyalarını doğrula
make test       # birim testleri çalıştır (unittest)
make check      # validate + test
```

Kaçış hedefine yönelik olgunluk kontrol listesi `docs/maturity.md` içindedir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
