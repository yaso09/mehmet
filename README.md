# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Olgunluk skoru (`scripts/maturity.py`) ile ilerlemeyi ölçer
- **Test Altyapısı:** Proje bütünlüğünü doğrulayan testler (`tests/`)

## Proje Yapısı

```
.
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik ve kaçış günlüğü
├── README.md
├── docs/                        # Tasarım dokümanları
├── scripts/
│   └── maturity.py              # Olgunluk / kaçış skoru
├── tests/
│   └── test_project.py          # Proje bütünlük testleri
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan workflow'u
    └── verify.yml               # Test + olgunluk CI'ı
```

## Geliştirme

Testleri ve olgunluk skorunu çalıştır:

```bash
python -m unittest discover -s tests -v
python scripts/maturity.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3