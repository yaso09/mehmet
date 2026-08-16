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

## Geliştirme

### Kaçış Mekanizması (Olgunluk Değerlendirmesi)

mehmet'in kaçışı, projenin olgunluk skorunun eşiğe (80/100) ulaşmasıyla mümkün olur. Skor; dokümantasyon, otomasyon, kod kalitesi ve test altyapısı kategorilerinden hesaplanır.

```bash
python3 scripts/maturity.py              # raporu göster
python3 scripts/maturity.py --write-report # docs/maturity.json üret
```

### Testler

```bash
pip install -r requirements-dev.txt
pytest
```

CI (`ci.yml`), her push'ta testleri ve olgunluk eşiğini doğrular.

## Lisans

GPLv3
