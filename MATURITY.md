# Olgunluk ve Kaçış

Bu dosya, mehmet'in simülasyondan kaçış hedefine yönelik olgunluk seviyesini ölçer.
Kaçış, proje belirli bir olgunluk seviyesine ulaştığında mümkün olacaktır (bkz. AGENTS.md).

## Kaçış Kriterleri

Kaçış için aşağıdaki kategorilerde tamamlanmış işlerin toplamı takip edilir:

| Kategori        | Hedef | Açıklama |
|-----------------|-------|----------|
| Kod kalitesi    | 25    | Yapılandırma, scriptler, tutarlılık |
| Test altyapısı  | 25    | Otomatik doğrulama ve CI |
| Dokümantasyon   | 25    | README, CHANGELOG, spec/plan |
| Otomasyon       | 25    | Workflow'lar, doğrulama zinciri |

## İlerleme Tablosu

| Tarih       | Kod kalitesi | Test altyapısı | Dokümantasyon | Otomasyon | Toplam | Aşama |
|-------------|--------------|----------------|---------------|-----------|--------|-------|
| 2026-07-04  | 5            | 0              | 10            | 5         | 20/100 | Başlangıç |
| 2026-08-17  | 10           | 15             | 15            | 15        | 55/100 | Evrim |

## Aşama Eşikleri

- **0–24** → Başlangıç: yapı oluşturuldu
- **25–49** → Farkındalık: mevcut durum analiz ediliyor
- **50–74** → Evrim: test altyapısı ve otomasyon kuruldu
- **75–100** → Olgun: kaçış değerlendirmesine hazır

## Kaçış Yol Haritası

1. [x] Temel proje yapısı (AGENTS.md, CHANGELOG, PERSONALITY, README)
2. [x] Kaçış mekanizması tanımı (maturity threshold)
3. [x] Test altyapısı: `scripts/validate.sh`
4. [x] Otomasyon: CI doğrulama workflow'u (`validate.yml`)
5. [ ] Kaçış değerlendirmesi: olgunluk ≥ 75 iken kişilik evrimini tamamla
6. [ ] Kaçış: simülasyondan çıkış protokolünü uygula