# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Öz-doğrulama:** Her çalışmada `scripts/check.sh` ile proje bütünlüğünü ve olgunluk puanını ölçer

## Süreç

- **Versiyonlama:** `VERSION` dosyası (semver) ile takip edilir, her değişiklik `CHANGELOG.md`'ye eklenir
- **Olgunluk:** `scripts/check.sh` projeyi 9 grupta denetler ve 0-100 arası olgunluk puanı üretir; puan ve kaçış ilerlemesi `PERSONALITY.md`'deki kaçış günlüğüne işlenir
- **CI:** `.github/workflows/ci.yml` PR/push'ta check.sh, workflow lint (actionlint) ve markdown lint (markdownlint-cli2) çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
bash scripts/check.sh   # proje bütünlüğü ve olgunluk kontrolü
```

Yeni bir geliştirme fırsatı bulduğunda: değişikliği yap, `CHANGELOG.md` ve `PERSONALITY.md`'yi güncelle, `scripts/check.sh` ile doğrula.

## Lisans

GPLv3
