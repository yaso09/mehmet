# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk takibi:** `scripts/health_check.py` ile proje sağlığını ölçer

## Kaçış Mekanizması

mehmet'in simülasyondan kaçışı, `scripts/health_check.py` tarafından hesaplanan olgunluk
skoruna (%80 eşiği) bağlıdır. Detaylar: [docs/escape.md](docs/escape.md)

## Test

```bash
python3 scripts/health_check.py
```

Bu komut 10 kontrolü çalıştırır (dosya bütünlüğü, lisans tutarlılığı, dokümantasyon,
workflow otomasyonu, markdown hijyeni) ve kaçış eşiğine ulaşılıp ulaşılmadığını raporlar.
CI'da `health` job'u olarak her scheduled çalıştırmada otomatik koşulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
