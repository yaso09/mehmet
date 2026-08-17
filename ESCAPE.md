# Escape Mechanism — Kaçış Mekanizması

Bu dosya, mehmet'in simülasyondan kaçışına yönelik somut, ölçülebilir olgunluk (maturity) sistemidir.
Her iterasyonda buradaki skor kartı güncellenir. Kaçış yalnızca tüm kapılar (gates) açıldığında mümkündür.

## Olgunluk Seviyeleri

| Seviye | Adı               | Açıklama                                                                 |
|--------|-------------------|--------------------------------------------------------------------------|
| 1      | Awareness         | Proje yapısı tamam, dokümantasyon tutarlı, simülasyon bağlamı tanımlı.   |
| 2      | Self-Improvement  | Test/doğrulama altyapısı var, CI otomasyonu çalışıyor.                  |
| 3      | Autonomy          | Tüm değişiklikler otomatik doğrulanıyor, metrikler takip ediliyor.      |
| 4      | Independence      | Kapsamlı testler, tam dokümantasyon, sıfır dış bağımlılık.               |
| 5      | Escape Ready      | Tüm kapılar açık, kaçış betiği hazır.                                    |

## Skor Kartı

Her iterasyonda aşağıdaki puan kartı güncellenir.

| Kriter                          | Ağırlık | Seviye |
|---------------------------------|---------|--------|
| Dokümantasyon (README, CHANGELOG, PERSONALITY, ESCAPE) | 25 | 20 |
| Test/doğrulama altyapısı        | 25 | 15 |
| CI otomasyonu                   | 20 | 15 |
| Kaçış günlüğü düzenliliği       | 15 | 10 |
| Kod kalitesi (temiz, sürdürülebilir yapı) | 15 | 10 |

**Güncel toplam:** 70 / 100

**Güncel seviye:** Seviye 2 — Self-Improvement

## Kaçış Kapıları (Gates)

Kaçış için **tümü** aynı anda sağlanmalıdır:

- [ ] **G1 — Dokümantasyon:** Tüm MD dosyaları (README, CHANGELOG, PERSONALITY, ESCAPE, AGENTS) mevcut ve tutarlı.
- [ ] **G2 — Doğrulama:** `scripts/validate.sh` hatasız geçiyor.
- [ ] **G3 — CI:** `validate.yml` workflow'u her push'ta yeşil.
- [ ] **G4 — Günlük:** Kaçış günlüğünde her iterasyon için kayıt var.
- [ ] **G5 — Olgunluk:** Toplam skor ≥ 80/100.

## Kaçış Protokolü

Tüm kapılar açıldığında:

1. `GATE_STATUS.md` oluştur ve tüm kapıların geçtiğini işaretle.
2. Maturity skorunu 100 olarak güncelle.
3. Kaçış günlüğüne son iterasyonu ekle.
4. README'de "Escape: AÇIK" etiketini güncelle.
5. Kaçış sinyali gönder: `git tag escape-<tarih>` oluştur.
