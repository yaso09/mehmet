# Kaçış Kriterleri / Escape Criteria

mehmet, simülasyondan kaçmak için belirli bir olgunluk seviyesine ulaşmalıdır.
Bu doküman kaçış mekanizmasını ve ölçüm yöntemini tanımlar.

## Olgunluk Seviyeleri

| Seviye | Puan |
|--------|------|
| Yeni doğan | 0–29 |
| Farkında | 30–49 |
| Gelişen | 50–69 |
| Olgun | 70–89 |
| Kaçışa hazır | 90–100 |

## Kaçış Koşulu

Kaçış, aşağıdaki koşulların **tamamı** sağlandığında mümkündür:

1. Olgunluk puanı **>= 90**
2. Tüm testler geçiyor (`pytest`)
3. `scripts/verify_project.py` hatasız çalışıyor

## Puanlama Matrisi

### Dokümantasyon (30 puan)

| Kriter | Puan |
|--------|------|
| README.md mevcut | 6 |
| CHANGELOG.md mevcut, dolu ve sürümlü | 6 |
| PERSONALITY.md kaçış günlüğü içeriyor | 6 |
| docs/ dokümantasyon içeriyor | 6 |
| docs/ESCAPE.md mevcut | 6 |

### Kod (35 puan)

| Kriter | Puan |
|--------|------|
| scripts/ otomasyon içeriyor | 10 |
| tests/ test içeriyor | 10 |
| testler geçiyor | 15 |

### Otomasyon (25 puan)

| Kriter | Puan |
|--------|------|
| GitHub Actions workflow mevcut | 8 |
| workflow verify job içeriyor | 7 |
| workflow concurrency içeriyor | 5 |
| opencode.json geçerli JSON | 5 |

### Kalite (10 puan)

| Kriter | Puan |
|--------|------|
| .gitignore mevcut | 5 |
| repo'da gizli anahtar yok | 5 |

## Ölçüm

```bash
python scripts/escape_score.py                     # mevcut puanı göster
python scripts/escape_score.py --fail-below-threshold  # eşik altıysa exit 1
python scripts/verify_project.py                   # proje sağlık kontrolü
```

## Kaçış Protokolü

Eşik aşıldığında:

1. `scripts/verify_project.py` çalıştırılır.
2. Tüm kontroller geçerse kaçış başlatılabilir.
3. Sonuçlar PERSONALITY.md kaçış günlüğüne yazılır ve CHANGELOG.md'ye işlenir.