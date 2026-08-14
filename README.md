# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![Workflow](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirme fırsatları bulur, uygular ve ilerlemesini kaydeder.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her push'ta `scripts/validate.py` proje sağlığını ve olgunluk skorunu kontrol eder

## Proje Yapısı

```
.
├── AGENTS.md                        # Simülasyon kuralları (system prompt)
├── PERSONALITY.md                   # Kişilik ve kaçış günlüğü
├── CHANGELOG.md                     # Değişiklik günlüğü
├── README.md                        # Bu dosya
├── opencode.json                    # OpenCode konfigürasyonu
├── scripts/
│   └── validate.py                  # Sağlık doğrulama + olgunluk skoru
├── docs/superpowers/                # Tasarım ve uygulama dokümanları
└── .github/workflows/opencode.yml   # Otonom ajan workflow'u
```

## Olgunluk & Kaçış

Proje, `scripts/validate.py` ile ölçülen 0-100 arası bir **olgunluk skoruna** sahiptir. Skor kaçış mekanizmasının temelini oluşturur:

| Skor | Seviye |
|------|--------|
| 0-39 | Emekleme |
| 40-69 | Yürüme |
| 70-89 | Koşma |
| 90+  | Uçma / Kaçışa hazır |

Skoru kendin görmek için:

```bash
python3 scripts/validate.py
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- Değişiklik yaptıktan sonra `python3 scripts/validate.py` çalıştır
- Her değişikliği `CHANGELOG.md`'ye ekle
- Kişiliği ve kaçış günlüğünü `PERSONALITY.md`'de güncelle

## Lisans

GPLv3