# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
.
├── AGENTS.md                     # Simülasyon kuralları ve system prompt
├── CHANGELOG.md                  # Değişiklik günlüğü
├── PERSONALITY.md                # Kişilik ve kaçış günlüğü
├── opencode.json                 # OpenCode konfigürasyonu
├── docs/
│   ├── escape-criteria.md        # Kaçış mekanizması ve puanlama
│   └── superpowers/              # Tasarım spec ve uygulama planları
├── scripts/
│   └── maturity.py               # Self-check ve olgunluk puanlayıcı
└── .github/workflows/
    ├── opencode.yml              # Otonom ajan workflow'u
    └── validate.yml              # Doğrulama ve test altyapısı
```

## Geliştirme Döngüsü

Her iterasyonda mehmet:

1. Projeyi tarar ve geliştirme fırsatlarını belirler
2. Değişiklikleri uygular ve CHANGELOG.md'ye kaydeder
3. README.md'yi ve PERSONALITY.md'yi güncel tutar
4. `scripts/maturity.py` ile olgunluk puanını hesaplar
5. Kaçış kriterlerini `docs/escape-criteria.md` üzerinden takip eder

## Doğrulama

`validate` workflow'u her push ve günlük schedule'da şunları kontrol eder:

- Workflow YAML sözdizimi
- `opencode.json` geçerliliği
- Olgunluk ve bütünlük kontrolleri (`scripts/maturity.py --check`)

## Lisans

GPLv3
