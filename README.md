# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Check:** `scripts/maturity.py` ile proje olgunluğunu 0-100 arası ölçer
- **CI Validation:** `validate` workflow'u her push/PR'da yapı ve testleri doğrular

## Olgunluk Sistemi

Proje, kaçış hedefine ulaşmak için `scripts/maturity.py` ile ölçülen bir olgunluk skoru (0-100) kullanır:

- Zorunlu dosyaların varlığı
- JSON/YAML yapı doğruluğu
- CHANGELOG sürüm geçmişi
- Dokümantasyon bölümleri (README, PERSONALITY, AGENTS)
- Test altyapısı ve scripts dizini

Eşik değer (`MEPHISTO_ESCAPE_THRESHOLD`, varsayılan 70) aşıldığında proje olgun kabul edilir.

## Test

```bash
python3 scripts/maturity.py
python3 -m unittest discover -s tests -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3