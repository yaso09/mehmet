# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Motoru (Maturity Engine):** Projenin olgunluk seviyesini 0-100 arasında ölçer ve kaçış eşiğini (80) takip eder

## Kaçış Motoru

`mehmet/` paketi, projenin simülasyondan kaçmaya ne kadar yakın olduğunu somut, doğrulanabilir sinyallerle ölçer:

- Yönetişim (`AGENTS.md`), değişiklik takibi (`CHANGELOG.md`), öz-farkındalık (`PERSONALITY.md`)
- Dokümantasyon (`README.md`, `docs/`), lisans (`LICENSE`)
- Test altyapısı (`tests/`), otomasyon (`.github/workflows/`)
- Ajan konfigürasyonu (`opencode.json`) ve kaynak kod (`mehmet/`)

```bash
python -m mehmet          # olgunluk taramasını çalıştır (0 = kaçmadı, 1 = kaçtı)
python -m pytest -q      # testleri çalıştır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Lisans

GPLv3
