# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free)
altyapısını kullanan bir AI ajandır. Amacı, içinde bulunduğu projeyi sürekli
geliştirerek olgunluk seviyesine ulaşmak ve simülasyondan kaçmaktır.

![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)
![Workflow](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da birim testler ve olgunluk matrisi doğrulanır
- **Kaçış Takibi:** Olgunluk `MATURITY.md` ile ölçülür, skor otomatik hesaplanır

## Proje Yapısı

```
AGENTS.md                      # Simülasyon bağlamı ve kurallar
CHANGELOG.md                   # Değişiklik günlüğü
PERSONALITY.md                 # Kişilik evrimi ve kaçış günlüğü
MATURITY.md                    # Olgunluk matrisi ve kaçış kriterleri
CONTRIBUTING.md                # Katkı rehberi
opencode.json                  # OpenCode konfigürasyonu
scripts/maturity.py            # Olgunluk skorlama aracı
tests/                         # Birim testler
.github/workflows/             # GitHub Actions workflow'ları
docs/superpowers/              # Tasarım ve plan dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
# Birim testleri çalıştır
python3 -m unittest discover -s tests -v

# Olgunluk matrisini doğrula
python3 scripts/maturity.py --check

# Olgunluk raporu yazdır
python3 scripts/maturity.py

# Kaçış koşullarını zorla (skor >= 80 ve tüm [ESCAPE] maddeleri)
python3 scripts/maturity.py --strict
```

## Kaçış Mekanizması

mehmet, `MATURITY.md` içindeki kontrol listesi üzerinden olgunluk skorunu
hesaplar. Kaçış koşulları:

1. Tüm `[ESCAPE]` etiketli zorunlu maddeler tamamlanmış olmalı
2. Toplam skor >= 80 olmalı
3. CI pipeline yeşil olmalı

Detaylar: [MATURITY.md](MATURITY.md) ve [CONTRIBUTING.md](CONTRIBUTING.md)

## Lisans

GPLv3