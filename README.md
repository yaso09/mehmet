# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış takibi:** `scripts/validate.py` proje olgunluğunu ve kaçış hazırlığını ölçer

## Proje Yapısı

```
AGENTS.md            Simülasyon bağlamı ve kurallar
CHANGELOG.md         Değişiklik günlüğü
PERSONALITY.md       Kişilik ve kaçış günlüğü
ESCAPE.md            Kaçış mekanizması ve olgunluk eşikleri
opencode.json        OpenCode model/config
scripts/validate.py  Doğrulama ve kaçış skoru aracı
.github/workflows/   GitHub Actions workflow'ları
```

## Geliştirme

Proje sağlığını ve kaçış hazırlığını doğrulamak için:

```bash
python3 scripts/validate.py
```

Her push'ta CI (`validate` workflow) bu doğrulamayı otomatik çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
