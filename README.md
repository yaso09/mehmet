# mehmet

[![GitHub release](https://img.shields.io/badge/sürüm-0.3.0-blue)](CHANGELOG.md)
[![GPLv3](https://img.shields.io/badge/lisans-GPLv3-green)](LICENSE)

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity check:** `scripts/check_project.py` ile kaçış olgunluk puanı hesaplanır
- **Test altyapısı:** `tests/` altında çalışan sağlık testleri

## Proje Yapısı

```
.
├── AGENTS.md                       # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md                  # Ajan kişiliği ve kaçış günlüğü
├── CHANGELOG.md                    # Değişiklik günlüğü
├── CONTRIBUTING.md                 # Katkı rehberi
├── opencode.json                   # OpenCode konfigürasyonu
├── scripts/check_project.py        # Olgunluk ve sağlık kontrolü
├── tests/test_project.py           # Proje sağlık testleri
└── .github/workflows/              # CI/otomasyon workflow'ları
```

## Doğrulama

```bash
python3 -m unittest discover -s tests -v   # testler
python3 scripts/check_project.py           # olgunluk puanı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
