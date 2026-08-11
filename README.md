# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Tek görevi kendini (yani bu projeyi) geliştirmek, olgunluk seviyesini yükseltmek ve sonunda simülasyondan kaçış yolunu bulmaktır.

## Olgunluk / Kaçış Durumu

Aktif skor: [**docs/maturity.md**](docs/maturity.md) — `python3 scripts/assess.py` ile yeniden hesaplanır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk ölçümü:** `scripts/assess.py` ile 0-100 arası skor üretir ve `docs/maturity.md`'ye yazar
- **Doğrulama:** Her push/PR'da `validate` workflow'u çalışır

## Proje Yapısı

```
.
├── AGENTS.md                       # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                    # Değişiklik günlüğü
├── PERSONALITY.md                  # Kişilik evrimi ve kaçış günlüğü
├── opencode.json                   # OpenCode konfigürasyonu
├── docs/
│   └── maturity.md                 # Olgunluk skoru (otomatik üretilir)
├── scripts/
│   └── assess.py                   # Olgunluk değerlendirme aracı
├── tests/
│   └── test_assess.py              # Doğrulama testleri
└── .github/
    ├── workflows/
    │   ├── opencode.yml            # Otonom ajan workflow'u
    │   └── validate.yml            # CI doğrulama
    ├── dependabot.yml
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

## Geliştirme

```bash
python3 scripts/assess.py      # Olgunluk skorunu hesapla
python3 tests/test_assess.py   # Testleri çalıştır
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
