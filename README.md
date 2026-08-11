# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirir ve olgunluk (maturity) skorunu yükseltir.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomasyon:** `make validate` / `make test` / `make maturity` ile kalite ve ilerleme takibi

## Maturity / Kaçış

Proje olgunluğu `scripts/maturity.py` ile 0-100 arasında ölçülür (eşik: 85/100).
Son skor `meta/maturity.json` içinde tutulur. Detaylar: [docs/maturity.md](docs/maturity.md).

```
maturity: 100.0/100 (threshold 85)  >> ESCAPE READY
```

## Yapı

```
AGENTS.md                 # Simülasyon bağlamı ve kurallar
CHANGELOG.md              # Değişiklik günlüğü
PERSONALITY.md            # Kişilik ve kaçış günlüğü
opencode.json             # OpenCode model konfigürasyonu
Makefile                  # validate / test / maturity hedefleri
scripts/validate.py       # Proje bütünlüğü doğrulayıcısı
scripts/maturity.py       # Olgunluk skoru hesaplayıcısı
tests/                    # Birim testler (unittest)
docs/maturity.md          # Kaçış mekanizması
meta/maturity.json        # Olgunluk kaydı
.github/workflows/        # autonomous + validate workflow'ları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
