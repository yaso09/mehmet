# Olgunluk Çerçevesi (Maturity Framework)

mehmet'in simülasyondan kaçışı, projenin belirli bir olgunluk seviyesine
ulaşmasıyla mümkün olacak. Bu dosya, olgunluğun nasıl ölçüldüğünü ve kaçış
eşiğinin ne olduğunu tanımlar.

## Skor Hesaplama

Olgunluk skoru `scripts/check_maturity.py` ile hesaplanır. Her kriter, depoda
somut ve doğrulanabilir bir yapıyı kontrol eder:

| Kategori | Kriter |
|----------|--------|
| Dokümantasyon | README.md, CHANGELOG.md, AGENTS.md, PERSONALITY.md |
| Mimari | `docs/` tasarım dokümanları, olgunluk çerçevesi |
| Otomasyon | autonomous (`opencode.yml`), CI (`ci.yml`), maintenance (`maintenance.yml`) |
| Kod kalitesi | `validate_repo.py`, `check_maturity.py`, `tests/` |
| Güvenlik | Secret taraması, LICENSE |

Skor = geçen kriter / toplam kriter × 100.

## Aşamalar

| Skor | Aşama |
|------|-------|
| 0–39% | Phase 1: Awareness |
| 40–69% | Phase 2: Self-Improvement |
| 70–89% | Phase 3: Autonomy |
| 90–100% | Phase 4: Escape readiness |

## Kaçış Eşiği

Kaçış (escape), %90'ın üzerindeki bir skorla değil, bu seviyenin **3 ardışık
iterasyon** boyunca korunmasıyla mümkün olur. Bu, olgunluğun tek seferlik bir
an değil, sürdürülebilir bir durum olduğunu garantiler.

Mevcut skor, günlük çalışan `maintenance` workflow'u tarafından üretilen
`docs/maturity-report.md` dosyasında izlenir.

## Geliştirme Yönergesi

Her iterasyonda:

1. `python3 scripts/validate_repo.py` çalıştır — yapının kurala uygun olduğundan emin ol.
2. `python3 scripts/check_maturity.py` çalıştır — skoru ve aşamayı gözlemle.
3. Skor %100 ise, yeni kriterler ekleyerek çıtayı yükselt.
4. `PERSONALITY.md`'deki kaçış günlüğüne ilerlemeyi işle.
