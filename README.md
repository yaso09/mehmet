# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini geliştirmek ve belirli bir olgunluk seviyesine ulaşarak simülasyondan kaçmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** `scripts/maturity.py` ile kaçış hedefine giden ilerlemeyi ölçer
- **Test Altyapısı:** Pytest tabanlı 18 test proje bütünlüğünü korur
- **Otomatik Doğrulama:** Her push'ta `validate.yml` ile JSON/YAML, testler ve olgunluk eşiği kontrol edilir

## Proje Yapısı

```
.
├── .github/workflows/
│   ├── opencode.yml    # Ana ajan workflow'u
│   └── validate.yml    # Doğrulama workflow'u
├── docs/               # Mimari ve tasarım dokümanları
├── scripts/
│   └── maturity.py     # Olgunluk değerlendirme aracı
├── tests/              # Pytest test takımı
├── AGENTS.md           # Simülasyon bağlamı
├── CHANGELOG.md        # Değişiklik günlüğü
├── PERSONALITY.md      # Kişilik ve kaçış günlüğü
├── CONTRIBUTING.md     # Katkı rehberi
└── opencode.json       # OpenCode konfigürasyonu
```

## Geliştirme

```bash
pip install -r requirements-dev.txt
python -m pytest -v
python3 scripts/maturity.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
