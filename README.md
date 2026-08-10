# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk ölçümü:** `scripts/maturity.py` ile kaçış eşiği takibi

## Mimari

```
.
├── AGENTS.md                     # Ajan simülasyon bağlamı ve kuralları
├── PERSONALITY.md                # Kişilik evrimi + kaçış günlüğü
├── CHANGELOG.md                  # Değişiklik günlüğü
├── opencode.json                 # OpenCode model/yapılandırma
├── scripts/maturity.py           # Olgunluk skoru (kaçış mekanizması)
├── tests/test_maturity.py        # Olgunluk script'i testleri
├── docs/                         # Tasarım ve uygulama dokümanları
└── .github/workflows/
    ├── opencode.yml              # Otonom ajan (10 dk'da bir)
    └── quality.yml               # CI: JSON/konfig test + test + olgunluk
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Olgunluk

Kaçış, projenin ölçülebilir olgunluğa ulaşmasıyla mümkündür. Skor 0-100'dur;
kaçış eşiği **≥ 95** ve tüm kontrol listelerinin tamamlanmasıdır.

```bash
python3 scripts/maturity.py       # olgunluk raporu
python3 scripts/maturity.py --json
python3 tests/test_maturity.py    # testleri çalıştır
```

## Lisans

GPLv3