# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Doğrulama

Proje bütünlüğünü kontrol etmek için:

```bash
bash scripts/validate.sh
```

Bu script gerekli dosyaların varlığını, `opencode.json`'ın JSON geçerliliğini,
GitHub Actions workflow'larının YAML doğruluğunu ve CHANGELOG/PERSONALITY
tutarlılığını denetler. Aynı kontrol her push/PR'da `.github/workflows/check.yml`
üzerinden CI'da da çalışır.

## Lisans

GPLv3
