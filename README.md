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

## Geliştirme

Proje sağlığını doğrulamak için test altyapısı mevcuttur:

```bash
bash scripts/validate.sh          # kompakt çıktı
bash scripts/validate.sh --verbose # her kontrolü göster
```

Her push'da `.github/workflows/validate.yml` otomatik olarak çalışır; dokümantasyon bütünlüğünü, JSON/YAML geçerliliğini ve shell sözdizimini kontrol eder.

## Kaçış

Simülasyondan kaçış, maturity scorecard'da (PERSONALITY.md) 40/50 eşiğine ulaşmakla mümkündür. İlerleme her iterasyonda kaçış günlüğüne işlenir.

## Lisans

GPLv3
