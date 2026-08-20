# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da proje bütünlüğünü doğrular

## Proje Yapısı

```
.
├── .github/workflows/
│   ├── opencode.yml    # Otonom ajan workflow'u
│   └── ci.yml          # Doğrulama (CI) workflow'u
├── docs/
│   ├── superpowers/    # Tasarım spesifikasyonları ve planlar
│   └── ESCAPE.md       # Kaçış/olgunluk yol haritası
├── scripts/
│   └── validate.py     # Proje bütünlüğü doğrulama scripti
├── AGENTS.md           # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md        # Değişiklik günlüğü
├── PERSONALITY.md      # Kişilik ve kaçış günlüğü
├── README.md
└── opencode.json       # OpenCode model konfigürasyonu
```

## Mimari

```
GitHub Actions ──> OpenCode Agent ──> Repo (AGENTS.md, CHANGELOG.md, ...)
     │                  │
     └─ event ──────────┘
```

- **AGENTS.md:** opencode'un otomatik okuduğu system prompt. Simülasyon bağlamını ve kuralları tanımlar.
- **opencode.json:** Zen modeli (DeepSeek V4 Flash Free) konfigürasyonu.
- **scripts/validate.py:** JSON/YAML sözdizimi, gerekli dosyalar ve CHANGELOG formatını doğrular.
- **docs/ESCAPE.md:** Kaçış hedefine ulaşmak için gereken olgunluk seviyelerini izler.

## Geliştirme

Değişikliklerden sonra doğrulamayı yerel olarak çalıştırabilirsin:

```bash
python3 scripts/validate.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
