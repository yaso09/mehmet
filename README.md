# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirir ve kendini evrimleştirir.

**Güncel sürüm: 0.3.0**

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** `scripts/validate.sh` ile proje sağlığı doğrulanır, CI'da otomatik çalışır
- **Kaçış mekanizması:** `MATURITY.md` rubriğinde ölçülen olgunluk skoru (90/100)

## Yapı

```
.
├── AGENTS.md                 # Simülasyon bağlamı ve kurallar
├── MATURITY.md               # Kaçış rubriği ve olgunluk skoru
├── PERSONALITY.md            # Kişilik ve kaçış günlüğü
├── CHANGELOG.md              # Değişiklik günlüğü
├── VERSION                   # Sürüm dosyası
├── opencode.json             # OpenCode konfigürasyonu
├── scripts/
│   └── validate.sh           # Proje sağlık kontrolü
└── .github/workflows/
    ├── opencode.yml          # Otonom ajan workflow'u
    └── ci.yml                # Push/PR doğrulama
```

## Doğrulama

```bash
bash scripts/validate.sh
```

Script, kritik dosyaların varlığını, sürüm tutarlılığını, kaçış günlüğünü ve konfigürasyon geçerliliğini kontrol eder.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3