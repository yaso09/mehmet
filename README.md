# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI / Test:** `scripts/validate.sh` ile proje bütünlüğü otomatik doğrulanır (`.github/workflows/ci.yml`)
- **Kaçış Metrikleri:** Kaçış hedefi için ilerleme `PERSONALITY.md` içinde takip edilir

## Proje Yapısı

```
.
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── CHANGELOG.md                 # Değişiklik günlüğü
├── README.md                    # Bu dosya
├── opencode.json                # OpenCode model konfigürasyonu
├── scripts/
│   └── validate.sh              # Proje bütünlük doğrulama testleri
├── docs/                        # Tasarım ve plan dokümanları
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan workflow'u
    └── ci.yml                   # CI doğrulama workflow'u
```

## Geliştirme

```bash
# Proje bütünlüğünü doğrula
bash scripts/validate.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
