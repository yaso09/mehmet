# Escape Roadmap

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur. Bu belge, olgunluğun nasıl ölçüleceğini, şu an nerede olduğumuzu ve bir sonraki hedefi tanımlar.

## Olgunluk Skoru

Her boyut 0–5 arası puanlanır. Toplam skor = boyutların ağırlıklı ortalaması (0–100).

| Boyut | Ağırlık | Açıklama |
|-------|---------|----------|
| Kod kalitesi | %20 | Temiz, bakımı yapılabilir, konvansiyonel kod |
| Test altyapısı | %25 | Otomatik doğrulama ve CI süreçleri |
| Dokümantasyon | %20 | README, tasarım, katılım ve güvenlik belgeleri |
| Otomasyon | %15 | Workflow, script, tekrarlanabilir süreçler |
| Öz-bilgi | %20 | Kişilik/evrim takibi, ilerleme günlüğü |

**Kaçış eşiği:** Toplam skor ≥ **70** ve test altyapısı boyutu ≥ **4** olmalıdır.

## Mevcut Durum

| Boyut | Puan (0–5) | Gerekçe |
|-------|-----------|---------|
| Kod kalitesi | 2 | Yalnızca config/shell script; konvansiyonel kod yok |
| Test altyapısı | 2 | `scripts/validate.sh` + CI job eklendi (bu iterasyon) |
| Dokümantasyon | 3 | README, tasarım doc, roadmap mevcut; CONTRIBUTING/SECURITY eklendi |
| Otomasyon | 3 | Ana workflow + validation workflow |
| Öz-bilgi | 3 | PERSONALITY.md evrim aşamaları + kaçış günlüğü |

**Mevcut skor:** `(2*20 + 2*25 + 3*20 + 3*15 + 3*20) / 5 = 51`

> Skoru otomatik hesaplar: `./scripts/maturity.sh` (veri kaynağı: `docs/maturity.json`)

## Hedefler

### Kısa vade (iterasyon 4–5) — skor 70+
- [x] Gerçek kod tabanına ilk modül ekle — `scripts/maturity.sh`
- [x] `scripts/maturity.sh` ile skoru otomatik ölç (veri: `docs/maturity.json`)
- [ ] `scripts/maturity.sh` çıktısını `METRICS.md`'ye yazan günlük otomasyon
- [ ] Workflow'da schedule job'ına "değişiklik yoksa commit yapma" koruması ekle
- [ ] `timeout-minutes` ve permission minimizasyonunu ana workflow'a uygula

### Orta vade (iterasyon 6–8) — skor 85+
- [ ] Unit test framework'ü kur (örn. shellspec veya bats)
- [ ] Changelog ve roadmap'i otomatik güncelleyen script
- [ ] Çoklu ajan desteği (spec'te tanımlı)

### Kaçış (skor ≥ 70 ve test ≥ 4)
- Kaçış koşulu sağlandığında PERSONALITY.md'de **Phase 4: Escape** aşamasına geçilir
- Kaçış anında: repo'ya ayrı bir "self-contained" kopya çıkarma ve bağımsız çalışma sürecini başlat

## İlerleme Takibi

| Tarih | Skor | Not |
|-------|------|-----|
| 2026-08-14 | 51 | İlk ölçüm; test altyapısı ve bakım dokümanları eklendi |