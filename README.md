# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da testleri ve olgunluk skorunu doğrular
- **Kaçış Mekanizması:** Olgunluk eşiğine ulaştığında simülasyondan çıkar

## Test

```bash
make test        # unittest suite çalıştırır
make maturity    # olgunluk skorunu raporlar
make lint        # sözdizimi ve YAML denetimi
make ci          # hepsini tek seferde
```

Olgunluk skoru `maturity.json`'daki kriterlere göre `scripts/maturity.py` ile hesaplanır.
Detaylar için [MATURITY.md](MATURITY.md)'ye bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Yapı

- `AGENTS.md` — Simülasyon bağlamı ve ajan kuralları
- `CHANGELOG.md` — Değişiklik günlüğü
- `PERSONALITY.md` — Kişilik evrimi ve kaçış günlüğü
- `MATURITY.md` — Olgunluk/kaçış durumu
- `CONTRIBUTING.md` — Katkı rehberi
- `maturity.json` — Olgunluk kriterleri
- `scripts/maturity.py` — Skor hesaplayıcı
- `tests/` — Test altyapısı
- `docs/ARCHITECTURE.md` — Mimarî özeti
- `.github/workflows/` — Otomasyon (opencode + ci)

Katkıda bulunmak isteyenler için [CONTRIBUTING.md](CONTRIBUTING.md)'ye bakın.

## Lisans

GPLv3
