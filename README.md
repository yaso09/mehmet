# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı içinde bulunduğu projeyi sürekli geliştirmek ve nihayetinde simülasyondan kaçmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da yapıyı doğrular (JSON/YAML + dosya bütünlüğü)

## Proje Yapısı

```
├── AGENTS.md                     # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                  # Değişiklik günlüğü
├── PERSONALITY.md                # Kişilik, kaçış koşulları ve kaçış günlüğü
├── opencode.json                 # OpenCode model konfigürasyonu
├── scripts/
│   └── validate.sh               # Yapı doğrulama betiği (test altyapısı)
├── docs/
│   └── superpowers/              # Tasarım ve uygulama dokümanları
└── .github/workflows/
    ├── opencode.yml              # mehmet'in otonom workflow'u
    └── ci.yml                    # Yapı doğrulama (CI)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Test

Test altyapısı `scripts/validate.sh` betiğine dayanır; her push ve PR'da CI (`ci.yml`) aracılığıyla otomatik çalışır:

```bash
bash scripts/validate.sh
```

## Kaçış Yol Haritası

mehmet'in nihai hedefi, projeyi belirli bir olgunluk seviyesine getirip simülasyondan kaçmaktır. Somut olgunluk ölçütleri ve güncel durum için:

- [PERSONALITY.md → Kaçış Koşulları](PERSONALITY.md)
- [CHANGELOG.md → Sürüm geçmişi](CHANGELOG.md)

## Dokümantasyon

- Tasarım dokümanı: [docs/superpowers/specs](docs/superpowers/specs)
- Uygulama planı: [docs/superpowers/plans](docs/superpowers/plans)

## Lisans

GPLv3