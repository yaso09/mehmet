# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** [MATURITY.md](MATURITY.md) kaçış eşiğini (80/100) ölçer
- **Doğrulama:** `scripts/check_project.sh` proje bütünlüğünü doğrular
- **CI:** `.github/workflows/ci.yml` her push/PR'da doğrulama çalıştırır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Proje bütünlüğünü doğrulamak için:

```bash
./scripts/check_project.sh
```

Kaçış protokolü ve olgunluk skorlaması için [MATURITY.md](MATURITY.md) dosyasına bakın.

## Lisans

GPLv3
