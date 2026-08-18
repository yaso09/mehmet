# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama (CI):** Proje yapısını ve olgunluk skorunu otomatik kontrol eder
- **Olgunluk Takibi:** Kaçış eşiğine ulaşma hedefini ölçülebilir hale getirir

## Proje Yapısı

```
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── MATURITY.md                  # Olgunluk modeli ve kaçış eşiği (80/100)
├── CHANGELOG.md                 # Değişiklik günlüğü
├── opencode.json                # OpenCode model konfigürasyonu
├── scripts/
│   └── validate_project.py      # Yapı doğrulama + olgunluk skorlayıcı
├── docs/superpowers/            # Tasarım ve uygulama dokümanları
└── .github/workflows/opencode.yml
```

## Geliştirme

Proje bütünlüğünü doğrulamak ve olgunluk skorunu görmek için:

```bash
python3 scripts/validate_project.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3