# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validate:** Her çalışmada repo bütünlüğünü `scripts/validate.sh` ile doğrular
- **Maturity:** `scripts/score.sh` ile olgunluk skorunu hesaplar ve `docs/progress.md`'ye işler

## Proje Yapısı

```
.
├── AGENTS.md                        # Simülasyon kuralları ve kaçış hedefi
├── PERSONALITY.md                   # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md                     # Değişiklik günlüğü
├── docs/
│   ├── maturity.md                  # Olgunluk kriterleri (escape rubric)
│   ├── progress.md                  # İterasyon bazlı skor takibi
│   └── superpowers/                 # Tasarım ve uygulama dokümanları
├── scripts/
│   ├── validate.sh                  # Repo bütünlük doğrulaması
│   └── score.sh                     # Olgunluk skoru hesaplayıcı (0-100)
└── .github/workflows/opencode.yml   # Ana workflow (validate + autonomous + comment)
```

## Kaçış Mekanizması

Kaçış, ölçülebilir bir olgunluk eşiğine ulaşınca mümkün olur:

- **Skor >= 80/100** (`bash scripts/score.sh`)
- **Validate hatasız** (`bash scripts/validate.sh`)
- **Son 3 iterasyonda skor artışı** (`docs/progress.md`)

Kriterler: [docs/maturity.md](docs/maturity.md) | Güncel skor: [docs/progress.md](docs/progress.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
