# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Doğrulama:** Her push/PR'da proje bütünlüğü `scripts/validate.py` ile kontrol edilir
- **İlerleme Takibi:** Olgunluk skoru ve kaçış eşikleri `METRICS.md`'de ölçülür

## Proje Yapısı

```
.
├── AGENTS.md              # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md           # Değişiklik günlüğü
├── PERSONALITY.md         # Kişilik evrimi ve kaçış günlüğü
├── METRICS.md             # Olgunluk skoru ve kaçış eşikleri
├── scripts/
│   └── validate.py        # Proje bütünlük doğrulayıcı
└── .github/workflows/
    ├── opencode.yml       # Otonom ajan iş akışı
    └── validate.yml       # CI doğrulama iş akışı
```

## Yerel Geliştirme

Proje bütünlük kontrollerini yerel olarak çalıştırın:

```bash
python3 scripts/validate.py
```

## Lisans

GNU GENERAL PUBLIC LICENSE (GPLv3)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
