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

Proje, kaçış hedefine yönelik olgunluk seviyesini ölçmek için otomatik doğrulama kontrolleri içerir:

- `scripts/self-check.sh` — zorunlu dosyaların varlığı, JSON/YAML geçerliliği ve CHANGELOG/PERSONALITY güncelliğini kontrol eder
- `.github/workflows/validate.yml` — her push ve PR'da self-check'i çalıştırır
- Ana workflow (`opencode.yml`) her çalıştığında self-check'i ön koşul olarak koşar

Yerelde çalıştırma:

```bash
./scripts/self-check.sh
```

## Lisans

GPLv3
