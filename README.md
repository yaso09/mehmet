# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** `tests/` dizini altında otomatik doğrulama
- **Olgunluk ölçümü:** `scripts/maturity.py` ile kaçış ilerlemesini takip eder
- **CI:** Her push/PR'de test ve olgunluk kontrolü çalışır

## Geliştirme

Testleri çalıştır:

```bash
python3 -m unittest discover -s tests -v
```

Olgunluk seviyesini ölç:

```bash
python3 scripts/maturity.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
