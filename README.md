# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

Proje, simülasyondan kaçış hedefine **MATURITY.md**'de tanımlı olgunluk modeliyle ölçülebilir şekilde ilerler. Kaçış eşiği **Seviye ≥ 4 ve skor ≥ 90**'dır.

- **Tek komutla doğrulama:** `make check`
- **Skor hesaplama:** `python3 scripts/check_maturity.py`
- **Test doğrulama:** `python3 -m unittest discover -s tests -q`
- **CI kalite kapısı:** `.github/workflows/check.yml`

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
AGENTS.md                        Simülasyon kuralları
MATURITY.md                      Olgunluk modeli ve kaçış eşiği
PERSONALITY.md                   Kişilik ve kaçış günlüğü
CHANGELOG.md                     Değişiklik günlüğü
Makefile                         Tek komutla doğrulama (make check)
scripts/check_maturity.py        Olgunluk skoru hesaplayıcı
tests/test_project.py            Doğrulama testleri
.github/workflows/opencode.yml   Otonom geliştirme workflow'u
.github/workflows/check.yml      Kalite kapısı
```

## Lisans

GPLv3
