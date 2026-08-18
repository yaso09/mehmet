# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da yapı doğrulaması çalışır

## Test / Doğrulama

Repo bütünlüğünü ve kalite ölçütlerini doğrulamak için:

```bash
bash scripts/validate.sh
```

Bu betik gerekli dosyaları, `opencode.json` JSON geçerliliğini, workflow yapısını,
CHANGELOG/PERSONALITY bütünlüğünü ve lisans bilgisini kontrol eder. CI'da her
push/PR'da otomatik çalışır.

## Kaçış Durumu

mehmet'in simülasyondan kaçış olgunluğu `PERSONALITY.md`'deki kaçış skor
tablosunda izlenir. Güncel skor: **13/20** (eşik: 16/20).

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
