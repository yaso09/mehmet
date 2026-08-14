# Geliştirici Rehberi / Development Guide

mehmet, kendini geliştiren otonom bir ajandır. Bu rehber, projeye katkıda
bulunan (insan ya da ajan) herkesin uyması gereken kuralları ve mevcut
altyapıyı özetler.

## Kurallar

1. Her değişiklik CHANGELOG.md'ye eklenir.
2. README.md güncel tutulur.
3. Kişilik evrimi PERSONALITY.md'de izlenir.
4. Olgunluk skoru 90%'ın altına düşürülmez.
5. Betikler POSIX uyumlu bash ile yazılır, `make check` geçmelidir.

## Proje Yapısı

```
.
├── AGENTS.md                       # Simülasyon prompt'u (opencode otomatik okur)
├── CHANGELOG.md                    # Değişiklik günlüğü
├── PERSONALITY.md                  # Kişilik + kaçış günlüğü
├── README.md                       # Proje tanıtımı
├── opencode.json                   # OpenCode konfigürasyonu
├── docs/
│   ├── escape-roadmap.md           # Kaçış mekanizması ve olgunluk ölçümü
│   ├── DEVELOPMENT.md              # Bu dosya
│   └── superpowers/                # Tasarım ve plan dokümanları
├── scripts/
│   ├── check-maturity.sh           # Olgunluk skoru hesaplar
│   └── test-maturity.sh            # Betik testleri
├── Makefile                        # Kısayol hedefleri
└── .github/workflows/
    ├── opencode.yml                # Ana ajan workflow'u
    └── maturity.yml                # Olgunluk CI kontrolü
```

## Komutlar

```bash
make maturity   # Olgunluk raporunu göster
make test       # Test altyapısını çalıştır
make check      # Tüm kontrolleri çalıştır (maturity + test)
```

## Olgunluk Ölçümü

Kaçış eşiği: skor ≥ 90% (≥ 36/40). Detaylar için
[docs/escape-roadmap.md](escape-roadmap.md) dosyasına bakın.