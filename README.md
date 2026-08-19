# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk ölçümü:** Kaçış mekanizması için ölçülebilir proje olgunluk skoru

## Proje Yapısı

```
├── mehmet/                # Python paketi (olgunluk değerlendirmesi)
│   ├── __init__.py
│   ├── maturity.py        # Olgunluk skorlama motoru
│   └── __main__.py        # CLI giriş noktası
├── tests/                 # pytest testleri
├── docs/                  # Tasarım dokümanları
├── .github/workflows/     # GitHub Actions otomasyonu
│   ├── opencode.yml       # Ajan workflow'u
│   └── ci.yml             # Lint + test + olgunluk doğrulama
├── AGENTS.md              # Simülasyon bağlamı
├── CHANGELOG.md           # Değişiklik günlüğü
├── PERSONALITY.md         # Kişilik ve kaçış günlüğü
├── pyproject.toml         # Paketleme ve araç yapılandırması
└── LICENSE                # GPLv3
```

## Olgunluk Skoru (Kaçış Mekanizması)

Proje olgunluk skoru 5 kategoride ölçülür (toplam 100 puan):

| Kategori | Maks | Açıklama |
|---|---|---|
| Kod | 30 | Kaynak dosya, satır, fonksiyon/sınıf sayısı |
| Test | 25 | Test dosyası, test fonksiyonu, pytest yapılandırması |
| Dokümantasyon | 20 | README, CHANGELOG, LICENSE, AGENTS, PERSONALITY |
| Otomasyon | 15 | CI workflow sayısı, lint+test işi, olgunluk doğrulama |
| Yönetişim | 10 | Versiyon geçmişi, ajan yönergesi |

**Kaçış eşiği:** 80/100 puana ulaşınca kaçış koşulu sağlanır.

### Kullanım

```bash
# Mevcut durumu değerlendir (0 çıkış kodu = kaçış koşulu sağlandı)
python -m mehmet .
python -m mehmet /path/to/repo

# Testler
pip install -e ".[test]"
pytest

# Lint
ruff check .
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
