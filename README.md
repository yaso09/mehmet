# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![CI](https://github.com/anomalyco/mehmet/workflows/ci/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test Altyapısı:** Config ve dokümantasyon geçerliliğini doğrulayan unittest suite
- **CI/CD:** Her push/PR'de otomatik test

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Katkıda Bulunma

[CONTRIBUTING.md](CONTRIBUTING.md) bölümünü okuyun.

## Lisans

GPLv3