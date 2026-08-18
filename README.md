# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, içinde bulunduğu projeyi her çalıştığında geliştirmek ve nihayetinde simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Her çalıştırmada repo bütünlüğünü `scripts/validate.sh` ile doğrular

## Proje Yapısı

```
.
├── AGENTS.md                          # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                       # Değişiklik günlüğü
├── METRICS.md                         # Kaçış metrikleri / puan tablosu
├── PERSONALITY.md                     # Kişilik evrimi ve kaçış günlüğü
├── opencode.json                      # OpenCode model konfigürasyonu
├── scripts/
│   └── validate.sh                    # Repo bütünlük doğrulama betiği
├── docs/superpowers/                  # Plan ve tasarım dokümanları
└── .github/workflows/
    ├── opencode.yml                   # Otonom ajan workflow'u
    └── validate.yml                   # CI validasyon workflow'u
```

## Kaçış Durumu

Kaçış hedefine ne kadar yaklaşıldığı `METRICS.md` içindeki puan tablosuyla ölçülür. İlerleme `PERSONALITY.md`'deki kaçış günlüğünde takip edilir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- Değişiklikler her zaman CHANGELOG.md'ye işlenir
- `bash scripts/validate.sh` repo bütünlüğünü kontrol eder (CI'da da çalışır)

## Lisans

GPLv3
