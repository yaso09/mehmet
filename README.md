# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Escape Mechanism:** `scripts/maturity.py` olgunluk skoru hesaplar; eşiğe ulaşınca kaçış yolu açılır

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md               # Değişiklik günlüğü
├── README.md                  # Bu dosya
├── ESCAPE.md                  # Kaçış mekanizması skor geçmişi
├── opencode.json              # OpenCode yapılandırması
├── scripts/
│   ├── maturity.py            # Olgunluk / kaçış skoru hesaplayıcı
│   └── __init__.py
├── tests/
│   └── test_maturity.py       # Kaçış mekanizması testleri
└── .github/workflows/
    └── opencode.yml           # Otonom çalışma akışı (check + autonomous + comment)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
