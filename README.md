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

Projenin sağlığını doğrulamak için test altyapısı ve olgunluk takibi mevcuttur:

```bash
make test       # Proje yapısı testleri (unittest)
make validate   # Workflow YAML dosyalarını doğrula
make maturity   # Olgunluk puanını hesapla ve METRICS.md'ye yaz
make all        # Üçünü birden çalıştır
```

- `tests/` — Proje yapısını, CHANGELOG/PERSONALITY/README tutarlılığını doğrular
- `scripts/maturity.py` — 0-100 arası ölçülebilir olgunluk puanı üretir, METRICS.md'ye kaydeder
- `.github/workflows/ci.yml` — Her push/PR'da testleri ve olgunluk kontrolünü çalıştırır

## Lisans

GPLv3
