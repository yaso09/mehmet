# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her koşuda proje sağlığını ve olgunluk skorunu test eder

## Proje Sağlığı

Her koşuda `scripts/validate_project.py` çalışır ve projenin olgunluk skorunu
ölçer. Skorlama tablosu ve kaçış eşiği (80/90) `METRICS.md`'de tanımlıdır.

```bash
python3 scripts/validate_project.py
python3 -m unittest tests.test_validate_project -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
