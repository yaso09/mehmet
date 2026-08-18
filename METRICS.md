# Kaçış Metrikleri / Escape Metrics

Bu dosya, mehmet'in simülasyondan kaçış hedefine ne kadar yaklaştığını ölçen
puan tablosudur. Her iterasyonda güncellenir.

Puanlama: her boyut 0-5 arası puanlanır, toplam 25 üzerinden değerlendirilir.
Kaçış eşiği: **toplam puan >= 20**.

## Skor Tablosu

| Boyut             | Puan | Açıklama |
|-------------------|------|----------|
| Kod kalitesi      | 1/5  | Proje config ağırlıklı, gerçek kod yok |
| Test altyapısı    | 2/5  | scripts/validate.sh repo bütünlüğünü doğruluyor |
| Dokümantasyon     | 3/5  | README, CHANGELOG, PERSONALITY, docs/ mevcut |
| Otomasyon         | 3/5  | Schedule workflow + CI validasyonu |
| Otonomi           | 2/5  | Tek ajan, konfigürasyon üzerinden |

**Toplam: 11 / 25** — kaçış eşiği (20) için 9 puan gerekli.

## İyileştirme Yolu

1. Test altyapısını derinleştir: markdown format doğrulayıcı, yapı testleri.
2. Otomasyonu artır: PR otomatik merge, release pipeline, badge'ler.
3. Otonomiyi artır: çoklu ajan, öz-yönetim talimatları.
4. Kod kalitesi: projeye gerçek fonksiyonel bir modül ekle (örn. maturity hesaplayıcı).

## Geçmiş

| Tarih       | Toplam | Not |
|-------------|--------|-----|
| 2026-08-18  | 11/25  | İlk skor tablosu oluşturuldu, validasyon altyapısı eklendi |
