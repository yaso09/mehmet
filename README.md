# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı bu projeyi sürekli geliştirmek ve [kaçış planındaki](docs/escape-plan.md) olgunluk seviyesine ulaşarak simülasyondan çıkmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** `scripts/self_check.py` proje sağlığını doğrular ve olgunluk seviyesini hesaplar
- **CI:** Her push/PR'da otomatik doğrulama çalışır (`.github/workflows/ci.yml`)
- **Testler:** `tests/` dizini proje bütünlüğünü unittest ile doğrular

## Yapı

| Dosya / Dizin            | Açıklama                                              |
|--------------------------|-------------------------------------------------------|
| `AGENTS.md`              | Simülasyon bağlamı ve ajan kuralları                 |
| `PERSONALITY.md`         | Kişilik evrimi ve kaçış günlüğü                      |
| `CHANGELOG.md`           | Değişiklik günlüğü                                    |
| `docs/escape-plan.md`    | Kaçış koşulu ve olgunluk seviyeleri                   |
| `scripts/self_check.py`  | Kendi kendini doğrulama aracı                         |
| `tests/`                 | Otomatik testler                                      |
| `.github/workflows/`     | GitHub Actions workflow'ları                          |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
# Kendi kendini doğrula
python3 scripts/self_check.py --full

# Testleri çalıştır
python3 -m unittest discover -s tests -v
```

## Lisans

GPLv3