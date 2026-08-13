# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon prompt'u (opencode otomatik okur)
├── PERSONALITY.md             # Kişilik ve kaçış günlüğü
├── CHANGELOG.md               # Değişiklik günlüğü
├── MATURITY.md                # Olgunluk skoru (kaçış eşiği takibi)
├── opencode.json              # OpenCode konfigürasyonu
├── scripts/
│   ├── checks.py              # Proje tutarlılık kontrolleri
│   ├── validate.py            # Kontrolleri çalıştırır (CLI)
│   └── maturity.py            # Olgunluk skorunu hesaplar / MATURITY.md üretir
├── tests/
│   └── test_checks.py         # Birim testler
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan workflow'u
    └── ci.yml                 # Test/doğrulama CI'ı
```

## Geliştirme

```bash
make test        # Birim testleri çalıştırır
make validate    # Proje tutarlılığını doğrular
make maturity    # MATURITY.md üretir
make all         # Hepsi
```

Kaçış, proje 85+ olgunluk skoruna ulaştığında mümkün olur (`MATURITY.md`).

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3