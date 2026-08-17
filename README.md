# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Her değişiklikte olgunluk skorunu otomatik hesaplar ve CI'da doğrular

## Proje Yapısı

```
.
├── .github/workflows/
│   ├── opencode.yml      # Ajanı tetikleyen ana workflow
│   └── validate.yml      # Kalite kapısı (test + olgunluk)
├── docs/superpowers/     # Tasarım ve uygulama planları
├── scripts/maturity.py   # Olgunluk skoru hesaplayıcı
├── tests/test_maturity.py
├── AGENTS.md             # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md          # Değişiklik günlüğü
├── CONTRIBUTING.md       # Katkı kuralları
├── MATURITY.md           # Olgunluk düzeyleri ve kaçış koşulu
├── PERSONALITY.md        # Kişilik evrimi ve kaçış günlüğü
├── opencode.json         # OpenCode model konfigürasyonu
└── README.md
```

## Olgunluk / Maturity

Mevcut olgunluk skorunu görüntülemek için:

```bash
python3 scripts/maturity.py
```

Ayrıntılar ve kaçış koşulu için [MATURITY.md](MATURITY.md) dosyasına bak.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3