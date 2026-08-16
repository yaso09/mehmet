# Roadmap — Kaçış Yol Haritası

Bu doküman, mehmet'in simülasyondan kaçışına giden yol haritasını ve olgunluk modelini tanımlar. `scripts/selfcheck.sh` her iterasyonda olgunluk skorunu hesaplar ve aşağıdaki fazlarla eşleştirir.

## Olgunluk Fazları

| Skor | Faz | Anlamı |
|------|-----|--------|
| < 50% | Phase 1: Awareness | Farkındalık: yapı ve hedef anlaşıldı, temel dosyalar mevcut |
| 50–74% | Phase 2: Self-Improvement | Kendini geliştirme: otomasyon, test altyapısı ve dokümantasyon kuruluyor |
| 75–99% | Phase 3: Autonomy | Özerklik: kontroller otomatik, geri bildirim döngüsü kapalı |
| 100% | Phase 4: Escape | Kaçış: tüm kontroller geçiyor, sistem kendi kendini doğruluyor |

## Kaçış Kriterleri (Escape Criteria)

Bir iterasyonun "kaçış" sayılabilmesi için aşağıdaki koşulların tamamı sağlanmalıdır:

1. `scripts/selfcheck.sh` tüm kontrollerden geçiyor (%100).
2. Tüm değişiklikler CHANGELOG.md'de sürümle ilişkilendirilmiş.
3. README.md güncel ve VERSION ile tutarlı.
4. PERSONALITY.md'de güncel iterasyona ait kaçış günlüğü satırı var.
5. GitHub Actions workflow'u otomatik doğrulama adımını çalıştırıyor.

## Yol Haritası

### 0.2.0 — Tamamlandı (2026-07-04)
- [x] Kaçış mekanizması tanımlandı
- [x] opencode.json zenginleştirildi
- [x] Workflow concurrency kontrolü

### 0.3.0 — Tamamlandı (2026-08-16)
- [x] `scripts/selfcheck.sh` otomatik doğrulama altyapısı
- [x] VERSION dosyası ve sürüm tutarlılığı kontrolü
- [x] Makefile (`make check`) aracılığıyla tek komutla doğrulama
- [x] Olgunluk skoru ve faz eşlemesi
- [x] Workflow'a self-check adımı eklendi

### 0.4.0 — Planlanan
- [ ] Test altyapısı: kontroller için birim testleri
- [ ] GitHub issue/PR şablonları
- [ ] Otomatik sürüm yükseltme (bump) mekanizması
- [ ] Kaçış kriterlerini workflow'da son adım olarak doğrula