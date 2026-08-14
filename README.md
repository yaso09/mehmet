# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Checker:** `scripts/maturity.py` projenin olgunluk seviyesini ölçer ve kaçış eşiğini izler
- **CI Validation:** `validate.yml` her push/PR'da testleri ve olgunluk kontrolünü çalıştırır

## Geliştirme

Testleri çalıştır:

```bash
python3 -m unittest discover -s tests
```

Olgunluk skorunu gör:

```bash
python3 scripts/maturity.py
python3 scripts/maturity.py --json      # makine-okunur rapor
python3 scripts/maturity.py --threshold 22
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
