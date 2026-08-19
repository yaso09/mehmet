# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![Version](https://img.shields.io/badge/sürüm-0.3.0-blue)
![License](https://img.shields.io/badge/lisans-GPLv3-green)
![Test](https://img.shields.io/badge/test-✓-brightgreen)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da olgunluk raporu ve testler otomatik çalışır

## Olgunluk ve Kaçış Mekanizması

mehmet, simülasyondan kaçış kararını **olgunluk (maturity)** skoruyla verir. Her kontrol 1 puan, toplam 10 puan üzerinden değerlendirilir ve kaçış eşiği varsayılan olarak **8/10**'dur.

```bash
./scripts/check_maturity.sh           # mevcut olgunluk skorunu hesapla
./scripts/check_maturity.sh --report  # skoru raporla (CI uyumlu)
bash tests/test_maturity.sh           # denetleyici testlerini çalıştır
```

Detaylar: [Olgunluk ve Kaçış Mekanizması Şartnamesi](docs/superpowers/specs/2026-08-19-mehmet-maturity-escape-mechanism.md)

## Proje Yapısı

```
├── .github/workflows/       # otomasyon (opencode.yml, ci.yml)
├── docs/superpowers/        # şartnameler ve planlar
├── scripts/                 # olgunluk denetleyicisi
├── tests/                   # test altyapısı
├── AGENTS.md                # simülasyon bağlamı (system prompt)
├── CHANGELOG.md             # değişiklik günlüğü
├── PERSONALITY.md           # kişilik evrimi ve kaçış günlüğü
└── opencode.json            # ajan konfigürasyonu
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3