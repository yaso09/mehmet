# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** `scripts/validate.sh` ile proje sağlığı otomatik doğrulanır (push/PR'de `validate` workflow'u ile)
- **Maturity Score:** Kaçış hedefine yönelik ilerleme 0-10 arası ölçülür (`Olgunluk Skoru`)

## Proje Yapısı

```
.
├── AGENTS.md                          # Simülasyon bağlamı ve ajan kuralları
├── PERSONALITY.md                     # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md                       # Değişiklik günlüğü
├── opencode.json                      # OpenCode proje yapılandırması
├── scripts/
│   └── validate.sh                    # Proje sağlık kontrolü + olgunluk skoru
├── docs/superpowers/
│   ├── plans/                         # Uygulama planları
│   └── specs/                         # Tasarım dokümanları
└── .github/workflows/
    ├── opencode.yml                   # Otonom ajan workflow'u
    └── validate.yml                   # CI doğrulama workflow'u
```

## Geliştirme

Proje sağlığını doğrulamak ve olgunluk skorunu görmek için:

```bash
./scripts/validate.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3