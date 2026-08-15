# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Push/PR'da proje bütünlüğünü doğrular (`scripts/validate.py`)

## Proje Yapısı

```
.
├── AGENTS.md                      # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md                   # Değişiklik günlüğü (her iterasyonda güncellenir)
├── PERSONALITY.md                 # Kişilik evrimi ve kaçış günlüğü
├── README.md                      # Proje tanıtımı
├── opencode.json                  # OpenCode model konfigürasyonu
├── scripts/
│   └── validate.py                # Proje bütünlük doğrulayıcı (std-lib, bağımlılıksız)
├── docs/
│   └── superpowers/               # Plan ve tasarım dokümanları
└── .github/
    └── workflows/
        ├── opencode.yml           # Otonom ajan workflow'u
        └── validate.yml           # CI bütünlük doğrulama workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
