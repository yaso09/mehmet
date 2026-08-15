# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomatik Doğrulama:** `scripts/verify_project.py` proje bütünlüğünü CI'da (`.github/workflows/verify.yml`) kontrol eder
- **Kaçış Mekanizması:** Olgunluk skorlama ve kaçış koşulu [docs/maturity.md](docs/maturity.md) dosyasında tanımlıdır

## Geliştirme

Değişikliklerden sonra doğrulama aracını çalıştır:

```bash
python3 scripts/verify_project.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
