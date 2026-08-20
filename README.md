# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![Validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

mehmet, `scripts/healthcheck.py` ile ölçülen bir **olgunluk skoru** hesaplar.
Skor 4 kategoriden oluşur: dokümantasyon, konfigürasyon, otomasyon ve kod kalitesi.

- Kaçış eşiği: **%80 olgunluk**
- Son rapor: `docs/maturity-report.json`
- İlerleme günlüğü: `PERSONALITY.md` → Kaçış Günlüğü

Geliştirme sırasında `make check` (sağlık/olgunluk) ve `make test` (birim testler) çalıştırarak güncel durumu görebilirsin.

## Proje Yapısı

```
├── AGENTS.md                     # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                  # Değişiklik günlüğü
├── PERSONALITY.md                # Kişilik evrimi + kaçış günlüğü
├── README.md                     # Proje dokümantasyonu
├── opencode.json                 # OpenCode konfigürasyonu
├── LICENSE                       # GPLv3
├── Makefile                      # Ortak geliştirme komutları
├── scripts/
│   └── healthcheck.py            # Sağlık + olgunluk kontrolü
├── docs/
│   ├── maturity-report.json      # Son olgunluk raporu (otomatik)
│   └── superpowers/              # Plan ve tasarım dokümanları
└── .github/
    └── workflows/
        ├── opencode.yml          # Otonom ajan workflow'u
        └── validate.yml          # CI doğrulama workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3