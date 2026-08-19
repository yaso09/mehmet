# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her 10 dakikada bir projeyi tarar, geliştirme fırsatları arar ve uygular.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kendi kendini doğrulama:** Her iterasyon sonrası `scripts/validate.sh` ile proje bütünlüğünü kontrol eder
- **CI:** PR ve push'larda otomatik doğrulama (`validate` workflow)

## Proje Yapısı

```
.
├── AGENTS.md                         # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md                      # Değişiklik günlüğü
├── PERSONALITY.md                    # Kişilik evrimi ve kaçış günlüğü
├── README.md                         # Bu dosya
├── docs/superpowers/                 # Tasarım ve uygulama dokümanları
├── opencode.json                     # OpenCode yapılandırması
├── scripts/validate.sh               # Proje bütünlük doğrulaması
└── .github/workflows/
    ├── opencode.yml                  # Ana ajan workflow'u
    └── validate.yml                  # CI doğrulama workflow'u
```

## Geliştirme

```bash
# Proje bütünlüğünü doğrula
bash scripts/validate.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3