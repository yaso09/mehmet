# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Kontrolü:** `scripts/health_check.py` proje bütünlüğünü CI'da otomatik doğrular

## Proje Yapısı

```
mehmet/
├── AGENTS.md                      # Simülasyon kuralları (system prompt)
├── opencode.json                  # OpenCode model yapılandırması
├── CHANGELOG.md                   # Değişiklik günlüğü
├── PERSONALITY.md                 # Kişilik evrimi ve kaçış günlüğü
├── docs/
│   ├── ROADMAP.md                 # Kaçış kriterleri ve ilerleme
│   └── superpowers/               # Tasarım ve uygulama dokümanları
├── scripts/
│   └── health_check.py            # Proje sağlık kontrolü
└── .github/workflows/
    ├── opencode.yml               # Otonom ajan ana workflow'u
    └── health.yml                 # Periyodik sağlık doğrulaması
```

## Kaçış Yol Haritası

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasına bağlıdır.
Somut kriterler için [docs/ROADMAP.md](docs/ROADMAP.md)'ye bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
