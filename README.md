# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her push'ta proje sağlığını kontrol eden CI işi çalışır
- **Kaçış Hedefi:** Ölçülebilir olgunluk kriterleri (bkz. `docs/maturity.md`)

## Proje Yapısı

```
├── AGENTS.md                          # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                       # Değişiklik günlüğü
├── PERSONALITY.md                     # Kişilik evrimi ve kaçış günlüğü
├── opencode.json                      # OpenCode model konfigürasyonu
├── docs/
│   ├── maturity.md                    # Olgunluk/kaçış mekanizması
│   └── superpowers/                   # Tasarım ve uygulama dokümanları
└── scripts/
    └── check.sh                       # Proje doğrulama betiği
```

## Test

```bash
bash scripts/check.sh
```

Zorunlu dosyaların varlığını, JSON/YAML geçerliliğini ve kritik içerikleri doğrular.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
