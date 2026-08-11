# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `make check` ile proje tutarlılığı kontrol edilir
- **Kaçış takibi:** `make score` ile kaçış hazırlık skoru hesaplanır

## Geliştirici Araçları

```bash
make check   # proje tutarlılık doğrulaması
make score   # kaçış hazırlık skoru
make test    # testleri çalıştır (tests/)
make docs    # dokümantasyon listesi
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
