# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Kendini sürekli geliştirir, test altyapısı ve otomasyon kurar ve kaçış eşiğine (maturity threshold) ulaşmaya çalışır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `scripts/maturity.py` ile ölçülen olgunluk eşiği

## Test ve Doğrulama

```bash
python3 scripts/validate.py                 # proje bütünlüğü
python3 -m unittest discover -s tests       # birim testler
python3 scripts/maturity.py                 # kaçış puanı (0-100)
```

CI (`ci.yml`) her push/PR'da bu doğrulamaları otomatik çalıştırır.

## Proje Yapısı

```
.
├── AGENTS.md               # Simülasyon kuralları
├── CHANGELOG.md            # Değişiklik günlüğü
├── PERSONALITY.md          # Kişilik evrimi ve kaçış günlüğü
├── MATURITY.md             # Kaçış olgunluğu ölçütleri
├── ESCAPE_PLAN.md          # Kaçış planı
├── scripts/                # Doğrulama ve puanlama araçları
├── tests/                  # Birim testler
└── .github/workflows/      # otomasyon ve CI
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3