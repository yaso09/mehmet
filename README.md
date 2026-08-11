# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Yapılan her değişiklik CI'da otomatik doğrulanır

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── opencode.json              # OpenCode yapılandırması
├── docs/superpowers/          # Tasarım ve uygulama dokümanları
├── scripts/
│   └── validate.sh            # Yerel doğrulama betiği
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan iş akışı
    └── validate.yml           # CI doğrulama iş akışı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Değişiklik yapmadan önce doğrulama betiğini çalıştır:

```bash
bash scripts/validate.sh
```

Betik şunları kontrol eder:

- Gerekli dosyaların varlığı (AGENTS.md, CHANGELOG.md, PERSONALITY.md, vb.)
- `opencode.json` geçerli JSON mu
- `.github/workflows/*.yml` dosyaları geçerli YAML mı
- CHANGELOG.md yapısı ve README.md lisans bilgisi

Aynı kontroller push/PR sonrası `.github/workflows/validate.yml` üzerinden CI'da da çalışır.

## Lisans

GPLv3
