# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-validation:** Her iterasyonda `scripts/validate.sh` ile proje sağlığını doğrular
- **Maturity tracking:** `docs/MATURITY.md` rubriği ile kaçış skorunu takip eder

## Olgunluk

Kaçış eşiği: **20/25** — Güncel skor: **18/25**

| Boyut | Puan |
|---|---|
| Dokümantasyon | 4/5 |
| Otomasyon | 4/5 |
| Test / Doğrulama | 3/5 |
| Konfigürasyon Hijyeni | 4/5 |
| Özerklik | 3/5 |

Detay: [docs/MATURITY.md](docs/MATURITY.md)

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik, evrim ve kaçış günlüğü
├── README.md                  # Proje tanıtımı
├── LICENSE                    # GPLv3
├── opencode.json              # OpenCode konfigürasyonu
├── scripts/
│   └── validate.sh            # Proje sağlık kontrolü
├── docs/
│   ├── MATURITY.md            # Olgunluk rubriği
│   └── superpowers/           # Tasarım ve plan dokümanları
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan workflow'u
    └── validate.yml           # Doğrulama CI workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
# Proje sağlık kontrolünü çalıştır
bash scripts/validate.sh
```

## Lisans

GPLv3