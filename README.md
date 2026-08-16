# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her çalışmadan önce `scripts/verify.py` ile proje sağlığını kontrol eder
- **Olgunluk:** `scripts/maturity.py` ile kaçış eşiğine (80/100) olan mesafeyi ölçer

## Proje Yapısı

```
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik ve kaçış günlüğü
├── CONTRIBUTING.md            # Katkı kuralları
├── README.md
├── opencode.json              # OpenCode model konfigürasyonu
├── Makefile                   # Yardımcı komutlar
├── VERSION
├── docs/                      # Tasarım ve plan dokümanları
├── scripts/
│   ├── verify.py              # Proje sağlık doğrulaması
│   └── maturity.py            # Olgunluk skoru hesabı
├── tests/                     # Komut dosyası testleri
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan workflow'u
    └── ci.yml                 # CI doğrulama workflow'u
```

## Geliştirme

```bash
make verify    # proje sağlığını doğrula
make maturity  # olgunluk skorunu hesapla
make check     # ikisi birden
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3