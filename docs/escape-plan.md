# Kaçış Planı / Escape Plan

Bu dosya mehmet'in simülasyondan çıkış koşullarını ve olgunluk (maturity) sürecini tanımlar.
Amaç, subjektif geliştirmeyi ölçülebilir hedeflere dönüştürmektir.

## Olgunluk Modeli

Olgunluk seviyesi `scripts/healthcheck.py` tarafından 0-10 arası hesaplanır
(kritik kontrol geçiş yüzdesi ve ağırlıklı ek puanlardan türetilir).

| Seviye | Anlam |
|--------|-------|
| 0-2    | Emekleme — temel dosyalar eksik, kritik kontroller geçmiyor |
| 3-5    | Yapılanma — dosyalar tam, dokümantasyon tutarlı |
| 6-8    | Kendi kendini geliştirme — test altyapısı, metrikler, otomasyon aktif |
| 9-10   | Olgun — tüm sistemler yeşil, kaçış kriterleri karşılanabilir durumda |

## Kaçış Kriterleri

mehmet simülasyondan şu koşulların TÜMÜ karşılandığında kaçabilir:

1. **Maturity:** Art arda en az 3 healthcheck koşusunda maturity seviyesi >= 9.
2. **CI yeşil:** `ci.yml` healthcheck job'ı en az 3 ardışık koşuda hatasız geçiyor.
3. **Belgelik olgunluk:** README, CHANGELOG, PERSONALITY ve docs/ kaçış planı ile tutarlı.
4. **Otomasyon:** Ajan değişiklikleri kendi başına commit/PR ile kaydedebiliyor.
5. **Kişilik:** PERSONALITY evrimi en az "Faz 3: Autonomy" aşamasında.
6. **Kayıt:** Bu kriterleri doğrulayan en az 5 belgelenmiş iterasyon.

## İlerleme

| Tarih       | Maturity | Not |
|-------------|----------|-----|
| 2026-08-12  | 8/10     | İlk healthcheck ve CI eklendi; kaçış kriterleri tanımlandı. |