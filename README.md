# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Tek görevi kendini (bu projeyi) sürekli geliştirmek ve simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Push/PR sonrası proje tutarlılığı otomatik doğrulanır

## Sürüm

Güncel sürüm: **0.3.0** (bkz. `VERSION`)

## Proje Yapısı

```
.
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── README.md                    # Bu dosya
├── VERSION                      # Merkezi sürüm numarası
├── Makefile                     # Otomasyon hedefleri
├── opencode.json                # OpenCode model konfigürasyonu
├── LICENSE                      # GPLv3
├── scripts/
│   ├── validate.py              # Proje tutarlılık doğrulama
│   └── escape_status.py         # Kaçış olgunluk skoru
├── docs/superpowers/            # Tasarım ve plan dokümanları
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan workflow'u
    └── ci.yml                   # CI doğrulama workflow'u
```

## Doğrulama

```bash
make validate   # proje tutarlılığını doğrular
make status     # kaçış olgunluk skorunu hesaplar
make all        # ikisini birden çalıştırır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3