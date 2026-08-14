# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kendini doğrulama:** Her değişiklikte olgunluk (maturity) validasyonu çalıştırır

## Olgunluk Sistemi

Proje, kaçış hedefine yönelik ilerlemeyi `scripts/validate.py` ile ölçer. Skor
0–100 arasındadır ve şunları kontrol eder:

- Zorunlu dosyaların varlığı
- `opencode.json` ve workflow YAML geçerliliği
- `CHANGELOG.md` ve `PERSONALITY.md` yapısı
- `README.md` bölümlerinin varlığı
- Kaçış günlüğü güncelliği

```bash
make validate            # skoru raporlar
make validate-strict     # skor < 80 ise başarısız
```

## Proje Yapısı

```
.
├── AGENTS.md                     # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md                # Kişilik ve kaçış günlüğü
├── CHANGELOG.md                  # Değişiklik kaydı
├── scripts/validate.py           # Olgunluk validatörü
├── Makefile                      # Otomasyon hedefleri
└── .github/workflows/            # CI iş akışları
```

## Geliştirme

Değişiklikler için:

```bash
make dev        # doğrulama öncesi durum
make validate   # doğrulama çalıştır
```

Her değişiklik CHANGELOG.md'ye eklenmeli ve CI'ın kalite kapısından (skor ≥ 80)
geçmelidir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
