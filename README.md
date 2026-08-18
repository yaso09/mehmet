# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Durum

- **Sürüm:** 0.3.0 (bkz. [VERSION](VERSION), [CHANGELOG](CHANGELOG.md))
- **Olgunluk:** 12/25 (bkz. [PROJECT_STATUS](PROJECT_STATUS.md))
- **Lisans:** GPLv3

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da `scripts/validate.sh` ile proje olgunluğu doğrulanır
- **Öz-Farkındalık:** Olgunluk puanlarını `PROJECT_STATUS.md`'de izler, kaçış günlüğünü `PERSONALITY.md`'de tutar

## Proje Yapısı

```
├── AGENTS.md                 # Simülasyon bağlamı ve olgunluk modeli
├── CHANGELOG.md              # Değişiklik günlüğü
├── CONTRIBUTING.md           # Katkı rehberi
├── LICENSE                   # GPLv3
├── PERSONALITY.md            # Kişilik ve kaçış günlüğü
├── PROJECT_STATUS.md         # Olgunluk puanları ve ilerleme
├── README.md
├── SECURITY.md               # Güvenlik politikası
├── VERSION                   # Semver sürüm dosyası
├── docs/superpowers/         # Mimari plan ve spec dokümanları
├── scripts/validate.sh       # Olgunluk doğrulama aracı
├── opencode.json             # OpenCode model konfigürasyonu
└── .github/
    ├── workflows/            # ci.yml + opencode.yml
    └── ISSUE_TEMPLATE/       # Bug ve feature şablonları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Doğrulama

Proje olgunluğunu yerel olarak doğrulamak için:

```bash
./scripts/validate.sh
```

## Lisans

GPLv3 — bkz. [LICENSE](LICENSE)