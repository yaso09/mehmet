# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)
![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Doğrulama:** Her push/PR'da config ve dokümantasyon tutarlılığı otomatik kontrol edilir

## Proje Yapısı

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/       # Bug ve özellik isteği şablonları
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── opencode.yml      # Ana ajan workflow'u
│       └── ci.yml            # Doğrulama CI'si
├── docs/                     # Tasarım spec'leri ve implementasyon planları
├── scripts/
│   └── validate.py           # Proje sağlık doğrulayıcı
├── AGENTS.md                 # Ajan simülasyon prompt'u
├── CHANGELOG.md              # Değişiklik günlüğü
├── PERSONALITY.md            # Kişilik ve kaçış günlüğü
├── opencode.json             # OpenCode konfigürasyonu
└── README.md
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Değişiklik yaptıktan sonra proje sağlık kontrolünü çalıştır:

```bash
python scripts/validate.py
```

Bu komut config (JSON/YAML) geçerliliğini, gerekli dokümantasyon bölümlerinin
varlığını, CHANGELOG tutarlılığını ve kaçış günlüğünü doğrular. Aynı kontroller
push/PR'da otomatik olarak CI'da çalışır.

## Kurallar

- Her değişiklik CHANGELOG.md'ye eklenir
- README.md güncel tutulur
- Kişilik PERSONALITY.md'de evrimleştirilir
- Doğrulama: `python scripts/validate.py` başarılı olmalı

## Lisans

GPLv3
