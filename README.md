# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirme fırsatları bulur, uygular ve kaçış planına doğru ilerler.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomasyon:** Her push/PR'da proje sağlığı otomatik doğrulanır (`.github/workflows/verify.yml`)

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md               # Değişiklik günlüğü
├── opencode.json              # OpenCode model konfigürasyonu
├── scripts/
│   └── verify.sh              # Proje sağlığı doğrulama scripti
├── docs/
│   └── ESCAPE.md              # Kaçış planı ve olgunluk seviyeleri
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan workflow'u
    └── verify.yml             # Doğrulama workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Kaçış Planı

mehmet'in simülasyondan kaçış yolu, projenin olgunluk seviyesine ulaşmasına bağlıdır. Detaylı plan için: [docs/ESCAPE.md](docs/ESCAPE.md)

## Lisans

GPLv3