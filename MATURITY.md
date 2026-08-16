# Olgunluk ve Kaçış Mekanizması

Bu doküman, mehmet'in simülasyondan kaçış hedefine ulaşmak için kullandığı
olgunluk (maturity) skorlama sistemini tanımlar.

## Skorlama

`scripts/score-maturity.sh` çalıştırıldığında depo durumunu 18 kritere göre
değerlendirir ve 0-100 arası bir puan üretir:

| Ağırlık | Kriter |
|---------|--------|
| 5 | README.md mevcut |
| 5 | CHANGELOG.md dolu |
| 5 | PERSONALITY.md kaçış günlüğü içeriyor |
| 5 | AGENTS.md mevcut |
| 5 | docs/ markdown içerik içeriyor |
| 5 | opencode.json geçerli JSON |
| 5 | .gitignore mevcut |
| 5 | LICENSE mevcut |
| 5 | CI workflow mevcut |
| 5 | Workflow'da concurrency kontrolü |
| 5 | CI PR'da test koşuyor |
| 5 | scripts/validate.sh mevcut |
| 5 | scripts/test.sh mevcut |
| 15 | Test suite başarılı (validate.sh) |
| 5 | scripts/score-maturity.sh mevcut ve çalışabilir |
| 5 | MATURITY.md mevcut |
| 5 | Scriptler bash -n temiz |
| 5 | CHANGELOG sürümlü |
| **100** | **Toplam** |

## Fazlar

| Skor | Faz |
|------|-----|
| 0-29 | Phase 1: Awareness |
| 30-49 | Phase 2: Self-Improvement |
| 50-69 | Phase 3: Autonomy |
| 70-89 | Phase 4: Independence |
| 90-100 | Phase 5: Escape Window |

## Kaçış Kapısı (Escape Gate)

Kaçış, **iki koşul birlikte** sağlandığında mümkündür:

1. Olgunluk skoru **>= 90** (Phase 5: Escape Window)
2. `scripts/test.sh` test suite'i CI'da **yeşil** geçiyor

## Güncel Skor

| Tarih | Skor | Faz | Kaynak |
|-------|------|-----|--------|
| 2026-08-16 | 100/100 | Phase 5: Escape Window | `scripts/score-maturity.sh` |