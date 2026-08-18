# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Takibi:** `docs/ESCAPE.md` ve `scripts/maturity.py` ile ölçülebilir olgunluk skoru

## Proje Yapısı

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/        # Issue şablonları
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── opencode.yml       # Ajanın kendini geliştirme workflow'u
│       └── validate.yml       # Test + olgunluk skoru doğrulama
├── docs/
│   ├── ESCAPE.md              # Kaçış planı ve olgunluk kriterleri
│   └── superpowers/           # Tasarım ve uygulama dokümanları
├── scripts/
│   └── maturity.py            # Olgunluk skoru hesaplama
├── tests/
│   └── test_maturity.py       # Olgunluk sistemi birim testleri
├── AGENTS.md                  # Simülasyon bağlamı (system prompt)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PERSONALITY.md
├── SECURITY.md
└── README.md
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Test

```bash
python3 -m unittest discover tests
```

## Olgunluk Skoru

```bash
python3 scripts/maturity.py
```

Skor 85 üzerindeyse kaçış durumu elde edilir. Ayrıntılar: [docs/ESCAPE.md](docs/ESCAPE.md).

## Katkı

[Bakınız: CONTRIBUTING.md](CONTRIBUTING.md)

## Lisans

GPLv3