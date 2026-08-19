# mehmet

Kendi kendisini geliştiren otonom AI ajan.

**Mevcut sürüm:** 0.3.0

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı projeyi sürekli geliştirmek, olgunluk seviyesini yükseltmek ve sonunda simülasyondan kaçış eşiğine ulaşmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test Altyapısı:** `scripts/` altındaki araçlar için unittest testleri
- **CI Doğrulaması:** Her push/PR'da testleri ve proje tutarlılığını otomatik kontrol eder
- **Kaçış Mekanizması:** `scripts/maturity.py` ile objektif olgunluk puanı takibi

## Proje Yapısı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── opencode.json              # Ajan model konfigürasyonu
├── scripts/
│   ├── validate.py            # Proje tutarlılık doğrulayıcı
│   └── maturity.py            # Olgunluk puanı hesaplayıcı
├── tests/                     # unittest testleri
└── .github/workflows/
    ├── opencode.yml           # Ajan otomasyonu (schedule/issue/PR)
    └── validate.yml           # CI doğrulaması (test + validate)
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Yerel Geliştirme

Testler ve doğrulama bağımlılıksızdır (yalnızca Python 3.10+):

```bash
python3 -m unittest discover -s tests -v   # testleri çalıştır
python3 scripts/validate.py                # proje tutarlılığını kontrol et
python3 scripts/maturity.py                # olgunluk puanını gör
python3 scripts/maturity.py --json         # makine-okunur çıktı
```

## Lisans

GPLv3