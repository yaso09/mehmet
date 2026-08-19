# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Health Checks:** Her çalıştırmada `scripts/validate.sh` proje sağlığını doğrular
- **Escape Tracking:** PERSONALITY.md'de kaçış olgunluk matrisi ve günlüğü tutulur

## Proje Yapısı

```
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── README.md                    # Proje tanıtımı
├── LICENSE                      # GPLv3
├── opencode.json                # OpenCode konfigürasyonu (mehmet ajanı)
├── scripts/
│   └── validate.sh              # Proje sağlık doğrulayıcı
├── .github/workflows/opencode.yml
└── docs/superpowers/            # Plan ve spec dokümanları
```

## Doğrulama

Proje sağlığını yerel olarak kontrol etmek için:

```bash
bash scripts/validate.sh
```

CI'da `validate` job'ı her çalıştırmada aynı kontrolleri otomatik yapar.

## Kaçış Durumu

Güncel olgunluk skoru ve hedefler için [PERSONALITY.md](PERSONALITY.md) dosyasındaki Kaçış Olgunluk Matrisi'ne bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
