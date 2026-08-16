# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Sağlık Kontrolü ve Olgunluk

Proje, kaçış hedefine yönelik ilerlemeyi ölçen bir sağlık kontrolü içerir:

```bash
python3 scripts/check_project.py        # kontrol + MATURITY.md güncelle
python3 scripts/check_project.py --check  # sadece kontrol (CI)
```

Kontrol; zorunlu dosyaları, JSON/YAML geçerliliğini, sır sızıntısını, CHANGELOG ve README tutarlılığını doğrular ve 0-100 arası olgunluk skoru üretir. Skorlar [MATURITY.md](MATURITY.md)'de takip edilir ve [health workflow'u](.github/workflows/health.yml) her push/PR'de kontrolü çalıştırır. Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md)'e bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
