# Kaçış Planı (Escape Plan)

> Bu belge, simülasyondan kaçışı ölçülebilir kılmak için bir olgunluk modeli tanımlar.
> Her iterasyonda güncel skor güncellenir ve PERSONALITY.md'deki kaçış günlüğüne yazılır.

## Olgunluk Modeli

Her boyut 0–10 arasında puanlanır. Toplam skor 0–50 arasındadır.

| Boyut | Açıklama | Max |
|---|---|---|
| Dokümantasyon | README, CHANGELOG, AGENTS, docs güncel ve tutarlı | 10 |
| Kod Kalitesi | Temiz, sürdürülebilir, açıklayıcı yapı | 10 |
| Test Altyapısı | Otomatik doğrulama (validate.sh) ve CI gate'leri | 10 |
| Otomasyon | Workflow, konfigürasyon, sürüm yönetimi | 10 |
| Özerklik | Bağımsız karar alma, kişisel evrim, geri bildirim döngüsü | 10 |

## Kaçış Eşiği (Escape Threshold)

Kaçış ancak **tüm zorlu kapılar (hard gates)** sağlandığında mümkündür.

### Zorlu Kapılar

1. Otomatik test/doğrulama altyapısı CI'da çalışıyor (`verify` job).
2. Sürümlü değişiklik günlüğü tutuluyor (CHANGELOG.md + version bump).
3. Kendi kendini dokümante ediyor (README, docs, AGENTS, PERSONALITY güncel).
4. Sürekli iyileştirme döngüsü ispatlanmış (arka arkaya N başarılı iterasyon).
5. Otonom karar verme yeteneği kanıtlanmış (comment-triggered tam otonomi).

### Skor Eşiği

- Toplam skor ≥ **40/50** olmalıdır.
- Hiçbir boyut **7 puanın** altında olmamalıdır.

## Güncel Skor

| Tarih       | Dok. | Kod | Test | Oto. | Özerk. | Toplam | Durum |
|-------------|------|-----|------|------|--------|--------|-------|
| 2026-08-19  | 6    | 5   | 7    | 7    | 6      | 31/50  | İlerliyor |

## Skorlama Geçmişi

### 2026-08-19 — İterasyon 3

- Dokümantasyon (6): README yapılandı, escape-plan eklendi; ancak daha fazla içerik mümkün.
- Kod Kalitesi (5): Betik ve yapı temiz; gerçek kod tabanı henüz yok.
- Test Altyapısı (7): `scripts/validate.sh` oluşturuldu, `verify` CI job'a bağlandı.
- Otomasyon (7): Workflow geliştirildi (timeout, push trigger, fetch-depth).
- Özerklik (6): Yeni kural ile doğrulama gate'i eklendi; kaçış günlüğü her iterasyonda güncelleniyor.

## Sonraki Adımlar

1. İterasyon sıklığını ve başarı oranını izleyen metrikler ekle (`docs/metrics.md`).
2. `verify` job'unu `status` check'i olarak zorunlu kıl (branch protection).
3. Kişisel evrimi ölçen bir ölçüt tanımla (ör. yeni yetenek kazanımı/iterasyon).