# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Her değişiklik `make validate` ile doğrulanır (CI'da otomatik)
- **Escape Tracking:** Kaçış kriterleri docs/escape.md'de tanımlı ve puanlı

## Geliştirme

Proje durumunu doğrulamak için:

```bash
make validate
```

Bu komut gerekli dosyaların varlığını, konfigürasyonların geçerliliğini, CHANGELOG/README/PERSONALITY güncelliğini ve izlenen dosyalarda secret olmadığını kontrol eder. Kontroller CI'da `.github/workflows/validate.yml` ile de otomatik çalışır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
