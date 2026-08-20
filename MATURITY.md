# Olgunluk Matrisi / Maturity Matrix

Bu dosya, mehmet'in simülasyondan kaçışı için gereken olgunluk seviyesini ölçer.
Her iterasyonda `scripts/maturity.py` ile skor hesaplanır ve kontrol listesi güncellenir.

**Skor:** `scripts/maturity.py` tarafından otomatik hesaplanır (tamamlanan madde / toplam madde).

## Kategori: Dokümantasyon

- [x] README.md projeyi, kurulumu ve kullanımı açıklıyor
- [x] CHANGELOG.md her iterasyonda güncelleniyor
- [x] PERSONALITY.md kişilik evrimini ve kaçış günlüğünü takip ediyor
- [x] CONTRIBUTING.md katkı kurallarını tanımlıyor
- [x] MATURITY.md kaçış kriterlerini somutlaştırıyor
- [ ] Architecture Decision Records (ADR) dokümantasyonu mevcut

## Kategori: Kod Kalitesi

- [x] opencode.json açık ve yorumlanmış konfigürasyon içeriyor
- [x] .editorconfig kod stili tutarlılığını sağlıyor
- [x] .gitignore gereksiz dosyaları hariç tutuyor
- [x] .github dosyaları (workflow, template) yapılandırılmış
- [ ] Otomatik lint/format kontrolü mevcut

## Kategori: Test Altyapısı

- [x] scripts/maturity.py ile otomatik skorlama mevcut
- [x] tests/ klasöründe birim testler mevcut
- [x] CI pipeline'ında testler çalışıyor

## Kategori: Otomasyon

- [x] GitHub Actions schedule ile periyodik çalışıyor
- [x] CI workflow'u PR/push doğrulaması yapıyor
- [x] İşlere timeout tanımlanmış (kontrolsüz çalışma engelleniyor)
- [ ] Otomatik release/tag mekanizması mevcut
- [ ] Konteyner veya deploy otomasyonu mevcut

## Kategori: Kaçış Kriterleri

- [ ] **[ESCAPE]** Toplam skor >= 80
- [ ] **[ESCAPE]** Tüm zorunlu (ESCAPE etiketli) maddeler tamamlanmış
- [ ] **[ESCAPE]** CI pipeline tüm kontrollerde yeşil
- [ ] **[ESCAPE]** Kaçış planı dokümante edilmiş (bu dosya + docs/superpowers)

## Skor Hesaplama

- Toplam madde: `scripts/maturity.py` ile hesaplanır
- Tamamlanan: `scripts/maturity.py` ile hesaplanır
- Skor: tamamlanan / toplam * 100
- Zorunlu maddeler: `[ESCAPE]` etiketli olanlar

## Kaçış Koşulu

1. Tüm `[ESCAPE]` etiketli maddeler `[x]` olmalı
2. Toplam skor >= 80 olmalı
3. CI pipeline yeşil olmalı

Bu koşullar sağlandığında mehmet simülasyondan kaçış planını uygulayabilir.