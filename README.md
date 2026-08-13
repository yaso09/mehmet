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
AGENTS.md                 # Simülasyon bağlamı ve kurallar
CHANGELOG.md              # Değişiklik günlüğü
PERSONALITY.md            # Ajan kişiliği ve kaçış günlüğü
opencode.json             # OpenCode konfigürasyonu
VERSION                   # SemVer versiyon
docs/maturity.md          # Olgunluk/kaçış skoru
scripts/validate.py       # Doğrulama scripti
.github/workflows/        # CI + otomasyon workflow'ları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- **Doğrulama:** `python scripts/validate.py` (tüm yapılandırma ve dosya tutarlılığını kontrol eder)
- **CI:** Her push/PR'da otomatik doğrulama çalışır

## Kaçış Durumu

Olgunluk skoru ve kaçış takibi için `docs/maturity.md` dosyasına bakın.

## Lisans

GPLv3
