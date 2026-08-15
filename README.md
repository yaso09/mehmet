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

## Doğrulama

Proje bütünlüğü `scripts/validate.sh` ile kontrol edilir; CI'da her push/PR'da otomatik çalışır.

```bash
scripts/validate.sh
```

Doğrulama: JSON geçerliliği, zorunlu dosyalar, CHANGELOG formatı, kaçış günlüğü, README bölümleri ve temiz git çalışma alanı.

## Lisans

GPLv3
