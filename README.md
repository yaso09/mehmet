# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Proje Yapısı

```
AGENTS.md                      Simülasyon bağlamı ve kurallar
PERSONALITY.md                 Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md                   Değişiklik günlüğü
scripts/escape_score.py        Kaçış olgunluk skoru (0-100)
scripts/check_project.py       Proje tutarlılık kontrolleri
tests/test_project.py          Bağımlılıksız unittest testleri
.github/workflows/opencode.yml Ana ajan workflow'u
.github/workflows/ci.yml       CI doğrulama workflow'u
```

## Doğrulama

```bash
python3 scripts/check_project.py   # tutarlılık kontrolleri
python3 tests/test_project.py      # testler
python3 scripts/escape_score.py    # kaçış olgunluk skoru
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
