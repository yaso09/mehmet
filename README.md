# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** `scripts/maturity.py` ile kaçış olgunluğu skoru hesaplanır ve takip edilir

## Maturity / Kaçış Mekanizması

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Olgunluk skoru altı boyutta ölçülür ve kaçış için %100 skor gerekir — bu, tek seferde değil yalnızca sürdürülen evrimle (en az 3 farklı günde çalışma) ulaşılabilir:

| Boyut | Ağırlık | Kontroller |
|-------|---------|------------|
| history | %25 | sürüm sayısı, kaçış günlüğü kayıtları, farklı günlerde evrim |
| docs | %20 | README, CHANGELOG, AGENTS, PERSONALITY, kaçış günlüğü |
| code | %15 | scripts/ altındaki Python betikleri (sözdizimi) |
| tests | %15 | CI workflow'u ve doğrulama betiği |
| automation | %15 | schedule/issue/PR/yorum tetikleyicileri, concurrency |
| governance | %10 | lisans, opencode.json, .gitignore, lisans tutarlılığı |

- `python3 scripts/maturity.py` — insan okunur rapor
- `python3 scripts/maturity.py --json` — makine okunur çıktı
- `python3 scripts/maturity.py --write` — sonucu `MATURITY.md`'ye yazar

## Doğrulama (CI)

`scripts/validate.py` proje sağlığını kontrol eder: zorunlu dosyalar, AGENTS kuralları,
CHANGELOG sürümlemesi, kaçış günlüğü, lisans tutarlılığı, JSON/YAML geçerliliği ve
betik sözdizimi. Her push/PR'da `.github/workflows/ci.yml` tarafından otomatik çalıştırılır.

```bash
python3 scripts/validate.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
├── AGENTS.md                      # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                   # Değişiklik günlüğü
├── PERSONALITY.md                 # Kişilik ve kaçış günlüğü
├── MATURITY.md                    # Olgunluk raporu (otomatik)
├── scripts/
│   ├── maturity.py                # Kaçış olgunluk skoru
│   └── validate.py                # Proje sağlık kontrolü
└── .github/workflows/
    ├── opencode.yml               # Otonom ajan workflow'u
    └── ci.yml                     # Doğrulama ve maturity CI
```

## Lisans

GPLv3
