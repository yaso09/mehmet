# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da otomatik doğrulama çalıştırır

## Proje Yapısı

```
.
├── AGENTS.md                     # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                  # Değişiklik günlüğü
├── PERSONALITY.md                # Kişilik evrimi ve kaçış günlüğü
├── README.md                     # Bu dosya
├── docs/
│   ├── escape-roadmap.md         # Olgunluk metrikleri ve kaçış eşiği
│   └── superpowers/              # Tasarım ve uygulama dokümanları
├── scripts/
│   └── validate.sh               # Proje doğrulama scripti
├── opencode.json                 # OpenCode yapılandırması
└── .github/workflows/
    ├── opencode.yml              # Ana ajan workflow'u
    └── ci.yml                    # CI doğrulama workflow'u
```

## Test

```bash
bash scripts/validate.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
