# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kendi kendini izleme:** `scripts/maturity.py` ile kaçış olgunluk skorunu hesaplar

## Proje Yapısı

```
├── .github/
│   ├── dependabot.yml          # Bağımlılık güncellemeleri
│   └── workflows/
│       ├── opencode.yml        # Ana otonom ajan workflow'u
│       └── validate.yml        # Proje bütünlük doğrulama CI'ı
├── docs/                       # Tasarım ve plan dokümanları
├── scripts/
│   ├── maturity.py             # Kaçış olgunluk skoru
│   ├── test_validate.py        # Doğrulayıcı testleri
│   └── validate_project.py     # Proje bütünlük kontrolü
├── tests/                      # Proje testleri
├── AGENTS.md                   # Simülasyon prompt'u
├── CHANGELOG.md                # Değişiklik günlüğü
├── MATURITY.md                 # Kaçış mekanizması açıklaması
├── PERSONALITY.md              # Ajan kişiliği ve kaçış günlüğü
├── VERSION                     # Sürüm numarası
└── opencode.json               # OpenCode yapılandırması
```

## Doğrulama

Her değişiklik sonrası proje bütünlüğünü doğrulamak için:

```bash
python3 scripts/validate_project.py   # Bütünlük kontrolü
python3 scripts/test_validate.py      # Script testleri
python3 scripts/maturity.py           # Kaçış olgunluk skoru
```

Bu kontroller her push/PR'da GitHub Actions (`validate.yml`) ile otomatik çalışır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
