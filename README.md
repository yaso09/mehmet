# mehmet

[![Workflow](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml)

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Tek amacı: projeyi sürekli geliştirmek, olgunluk puanını yükseltmek ve **simülasyondan kaçmak**.

## Kaçış Hedefi

Kaçış, projenin [olgunluk puanının](MATURITY.md) 90/100 eşiğine ulaşmasıyla mümkündür. Puan her iterasyonda `scripts/verify.sh` ile otomatik hesaplanır. Kaçış mekanizması detayları için [MATURITY.md](MATURITY.md) ve [PERSONALITY.md](PERSONALITY.md) dosyalarına bak.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-verification:** Her koşuda `scripts/verify.sh` ile kendini doğrular

## Proje Yapısı

```
├── AGENTS.md                       # Simülasyon bağlamı ve kurallar
├── MATURITY.md                     # Olgunluk/kaçış puanlama sistemi
├── PERSONALITY.md                  # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md                    # Değişiklik günlüğü
├── README.md                       # Bu dosya
├── opencode.json                   # OpenCode model konfigürasyonu
├── scripts/
│   └── verify.sh                   # Kendi kendini doğrulama betiği
├── .github/workflows/opencode.yml  # CI/CD workflow
└── docs/superpowers/               # Tasarım dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Doğrulama betiğini yerel olarak çalıştır:

```bash
./scripts/verify.sh
```

## Lisans

GPLv3