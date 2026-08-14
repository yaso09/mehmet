# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Test

Proje bütünlüğü `tests/test_project.py` ile doğrulanır:

```bash
make test        # test suite'i çalıştır
make validate    # tam doğrulama (config + workflow + testler)
```

CI, her çalıştırmada `validation` job'ı ile bu testleri otomatik koşar.

## Proje Yapısı

```
AGENTS.md                     Simülasyon kuralları ve kaçış hedefi
MATURITY.md                   Olgunluk metrikleri ve kaçış eşiği
PERSONALITY.md                Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md                  Değişiklik günlüğü
tests/test_project.py         Bütünlük test suite'i
scripts/validate.sh           Doğrulama script'i
.github/workflows/opencode.yml  Otonom ajan workflow'u
```

## Lisans

GPLv3
