# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Motoru:** `scripts/maturity.py` ile projenin olgunluk puanını (0-100) ölçer

## Geliştirme

```bash
# Testleri çalıştır
python3 -m unittest discover -s tests -v

# Olgunluk puanını ölç (kaçış eşiği: 80)
python3 scripts/maturity.py

# Makine-okunur çıktı
python3 scripts/maturity.py --json
```

Testler ve olgunluk motoru, her push/PR'da `.github/workflows/ci.yml` ile CI'da otomatik çalışır.

## Kaçış Eşiği

Olgunluk puanı ≥ 80 olduğunda proje **escape-ready** kabul edilir. Detaylar için `AGENTS.md` ve `docs/` dosyalarına bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
