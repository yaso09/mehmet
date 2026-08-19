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
├── AGENTS.md                        # Simülasyon bağlamı ve ajan kuralları
├── PERSONALITY.md                   # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md                     # Değişiklik günlüğü
├── opencode.json                    # OpenCode model konfigürasyonu
├── scripts/validate.py              # Proje sağlık kontrolü + maturity skoru
├── docs/superpowers/                # Tasarım ve uygulama dokümanları
└── .github/workflows/
    ├── opencode.yml                 # Ana otonom ajan workflow'u
    └── validate.yml                 # CI: proje bütünlüğü doğrulama
```

## Doğrulama

Proje bütünlüğü `scripts/validate.py` ile doğrulanır; her PR ve push'ta CI otomatik çalıştırır.

```bash
python3 scripts/validate.py
```

## Lisans

GPLv3
