# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

mehmet, projenin olgunluk seviyesini `scripts/maturity.py` ile ölçer. Skor 0-100
arasındadır; 90 ve üzeri **kaçış eşiği** olarak kabul edilir. Detaylar için
[docs/maturity.md](docs/maturity.md).

```bash
python scripts/maturity.py            # olgunluk raporu
python scripts/maturity.py --json     # makine-okur JSON rapor
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Test altyapısı `pytest` üzerine kuruludur:

```bash
pip install -r requirements-dev.txt
pytest
```

## Proje Yapısı

```
.
├── .github/workflows/
│   ├── opencode.yml          # mehmet otonom ajan workflow'u
│   └── ci.yml                # test workflow'u
├── docs/
│   ├── maturity.md           # olgunluk modeli ve kaçış eşiği
│   └── superpowers/          # tasarım spec ve uygulama planı
├── scripts/
│   └── maturity.py           # maturity/kaçış otomasyonu
├── tests/
│   └── test_maturity.py      # maturity testleri
├── AGENTS.md                 # simülasyon bağlamı
├── CHANGELOG.md              # değişiklik günlüğü
├── PERSONALITY.md            # kişilik ve kaçış günlüğü
└── opencode.json             # opencode model konfigürasyonu
```

## Lisans

GPLv3
