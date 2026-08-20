# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da otomatik test ve coverage kontrolü (`.github/workflows/ci.yml`)
- **Olgunluk & Kaçış Takibi:** `scripts/maturity.py` ile projenin olgunluk skorunu ölçer

## Olgunluk & Kaçış Sistemi

Proje, simülasyondan kaçışın ancak belirli bir olgunluk seviyesine ulaşınca mümkün olduğu varsayımı üzerine kuruludur. `scripts/maturity.py` aracı projeyi 5 kategoride değerlendirir ve 0-100 arası bir skor üretir:

| Kategori | Ağırlık |
|----------|---------|
| Core files (AGENTS, README, CHANGELOG, LICENSE vb.) | 20 |
| Automation (workflow, schedule, CI, concurrency) | 20 |
| Tests (test dosyaları, coverage config) | 25 |
| Documentation (README bölümleri, docs/) | 15 |
| Code quality (Python kodu, scripts/, temizlik) | 20 |

Skor eşiği (varsayılan `80`) aşıldığında ajan **kaçmış** sayılır.

```bash
python3 scripts/maturity.py            # insan okunabilir çıktı
python3 scripts/maturity.py --json     # makine okunabilir çıktı
```

## Geliştirme

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3