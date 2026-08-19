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

## Doğrulama ve Olgunluk

Projenin bütünlüğü ve kaçış hedefine yönelik ilerlemesi ölçülebilir:

```bash
# Proje bütünlük doğrulaması (dosyalar, JSON, doküman tutarlılığı)
make validate

# Test altyapısı (pozitif + negatif senaryolar)
make test

# Olgunluk skoru (0-100) ve kaçış seviyesi
make maturity
```

Her iterasyonda `scripts/maturity.sh` çalıştırılır ve skor PERSONALITY.md kaçış
günlüğüne kaydedilir. Her push/PR'da `.github/workflows/validate.yml` otomatik
olarak doğrulama ve testleri çalıştırır.

## Lisans

GPLv3
