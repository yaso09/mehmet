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

```bash
# Repo sağlığı testleri
python3 -m unittest discover -s tests -v

# Olgunluk / kaçış skoru
python3 scripts/check-maturity.py

# Tüm workflow'ları lint'le
yamllint .github/workflows
```

CI, her push ve PR'da testleri ve olgunluk kontrolünü otomatik çalıştırır.
Kaçış kriterleri ve skorlama hakkında ayrıntı için [docs/maturity.md](docs/maturity.md) bölümüne bak.

## Lisans

GPLv3
