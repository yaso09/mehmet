# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.py` proje bütünlüğünü kontrol eder (CI'da otomatik)
- **Maturity/Kaçış:** `scripts/maturity.py` olgunluk skorunu hesaplar ve kaçış eşiğini izler

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── opencode.json              # OpenCode konfigürasyonu
├── docs/                      # Tasarım ve plan dokümanları
├── scripts/
│   ├── maturity.py            # Olgunluk skoru / kaçış eşiği
│   └── validate.py            # Proje tutarlılık doğrulaması
└── .github/workflows/
    ├── opencode.yml           # Otonom ajan workflow'u
    └── validate.yml           # CI doğrulama workflow'u
```

## Doğrulama ve Maturity

```bash
# Proje tutarlılığını kontrol et
python3 scripts/validate.py

# Maturity skorunu hesapla (insan-okunur)
python3 scripts/maturity.py

# Maturity skorunu JSON olarak al
python3 scripts/maturity.py --json
```

Kaçış, projenin belirli bir olgunluk seviyesine (`ESCAPE_THRESHOLD`, varsayılan %80) ulaşmasıyla mümkün olur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
