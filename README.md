# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Geliştirici Araçları

- **Olgunluk skoru:** `python3 scripts/maturity.py` — projeyi beş kategoride puanlar ve kaçış eşiğini (varsayılan 85) denetler. Fazlar: Farkındalık → Kendini Geliştirme → Özerklik → Kaçış.
- **Proje validasyonu:** `python3 scripts/validate.py` — zorunlu dosyaları, JSON/YAML geçerliliğini, CHANGELOG formatını, lisans tutarlılığını ve gizli bilgi sızıntılarını denetler.
- **Testler:** `python3 -m unittest discover -s tests -v` — birim testleri.

Her Push ve PR'da [CI workflow'u](.github/workflows/ci.yml) testleri, validasyonu ve olgunluk skorunu otomatik çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
