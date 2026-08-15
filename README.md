# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, içinde bulunduğu projeyi sürekli geliştirmek ve simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push'ta repo sağlık kontrolü çalışır (`.github/workflows/validate.yml`)
- **Kaçış Mekanizması:** Ölçülebilir olgunluk eşiği (`docs/escape-mechanism.md`)

## Proje Yapısı

```
.
├── AGENTS.md                       # Simülasyon prompt'u (opencode otomatik okur)
├── CHANGELOG.md                    # Değişiklik günlüğü
├── PERSONALITY.md                  # Kişilik evrimi ve kaçış günlüğü
├── README.md                       # Bu dosya
├── opencode.json                   # Model & ajan konfigürasyonu
├── scripts/
│   └── check.sh                    # Repo sağlık kontrolü
├── docs/
│   ├── escape-mechanism.md         # Kaçış eşiği ve olgunluk metrikleri
│   └── superpowers/                # Tasarım ve plan dokümanları
└── .github/workflows/
    ├── opencode.yml                # Ajan workflow'u (schedule/issue/PR/comment)
    └── validate.yml                # CI sağlık kontrolü
```

## Geliştirme

Değişiklik yapmadan önce repo sağlık kontrolünü çalıştır:

```bash
./scripts/check.sh
```

Kontrol şunları doğrular: gerekli dosyaların varlığı, `opencode.json` JSON
geçerliliği, workflow YAML sözdizimi, kaçış günlüğü ve sızmış secret yokluğu.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3