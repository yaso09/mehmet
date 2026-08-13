# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Score:** Kaçış eşiğini ölçer (MATURITY.md, 80/100)
- **Doğrulama:** `make validate` ile proje bütünlüğünü CI'da kontrol eder

## Geliştirici Araçları

```bash
make validate   # Proje bütünlüğünü doğrula
make score      # Olgunluk skorunu göster
make doctor     # Ortam kontrolü
make help       # Tüm komutları listele
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
