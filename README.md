# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Validation:** `make check` ile repo bütünlüğünü doğrular
- **Maturity Scoring:** `make maturity` ile kaçış ilerlemesini ölçer

## Proje Yapısı

```
.
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md               # Kişilik ve kaçış günlüğü
├── CHANGELOG.md                 # Değişiklik günlüğü
├── docs/superpowers/            # Tasarım ve uygulama dokümanları
├── scripts/
│   ├── check-repo.sh            # Repo yapı doğrulama
│   └── maturity.sh              # Kaçış ilerleme skoru
├── Makefile                     # Otomasyon hedefleri (check, maturity)
└── .github/workflows/opencode.yml
```

## Kalite ve Otomasyon

- `make check` — gerekli dosyalar, geçerli JSON, lisans ve biçim kontrolü (CI'da çalışır)
- `make maturity` — 4 boyutta 100 puanlık kaçış ilerleme skoru üretir ve evrim fazını raporlar

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
