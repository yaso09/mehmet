# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış İzleme:** `scripts/assess.py` projenin olgunluk seviyesini ölçer (0-100)

## Geliştirme

Testleri çalıştırmak ve olgunluk skorunu görmek için:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/assess.py
```

CI (`assess.yml`) her push'ta testleri ve olgunluk değerlendirmesini otomatik çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
