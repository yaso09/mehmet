# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış mekanizması:** `scripts/maturity.py` ile kaçış olgunluğunu ölçer
- **Otomasyon:** `scripts/validate.py` ile proje bütünlüğünü CI'da doğrular

## Proje Yapısı

```
├── scripts/                  # Yardımcı script'ler
│   ├── validate.py           # Proje bütünlük doğrulayıcı
│   └── maturity.py           # Kaçış olgunluk skorlayıcı
├── tests/                    # Unit testler (unittest, bağımsız)
├── .github/workflows/
│   ├── opencode.yml          # Otonom ajan workflow'u
│   └── validate.yml          # CI doğrulama workflow'u
├── AGENTS.md                 # Simülasyon bağlamı / ajan kuralları
├── PERSONALITY.md            # Kişilik ve kaçış günlüğü
├── CHANGELOG.md              # Değişiklik günlüğü
└── docs/                     # Tasarım ve plan dokümanları
```

## Geliştirme

```bash
# Proje bütünlüğünü doğrula
python3 scripts/validate.py

# Kaçış olgunluğunu raporla
python3 scripts/maturity.py

# Testleri çalıştır (harici bağımlılık yok)
python3 -m unittest discover -s tests -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
