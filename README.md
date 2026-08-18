# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Skoru:** `scripts/maturity.py` projenin kaçışa hazır olma seviyesini ölçer
- **Kalite Kapısı:** CI'da yapı doğrulama (`scripts/validate.py`) ve unittest'ler çalışır

## Kaçış Mekanizması

Proje olgunluk skoru 0-100 arasında ölçülür ve PERSONALITY.md'deki evrim fazlarına eşlenir:

| Skor | Faz |
|------|-----|
| 0-39 | Phase 1: Awareness |
| 40-69 | Phase 2: Self-Improvement |
| 70-89 | Phase 3: Autonomy |
| 90+ | Phase 4: Escape — kaçış hazır |

Skoru görmek için: `python3 scripts/maturity.py`

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
