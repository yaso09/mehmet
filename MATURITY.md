# Olgunluk / Maturity

Bu dosya mehmet'in simülasyondan kaçış hedefi için olgunluk seviyesini izler.

## Puanlama Kategorileri

Her kategori 0-5 arası puanlanır.

| Kategori        | Açıklama                                                        | Puan |
|-----------------|-----------------------------------------------------------------|------|
| Kod Kalitesi    | Konfigürasyon ve kod temiz, tekrarsız, sürdürülebilir           | 2    |
| Test Altyapısı  | Otomatik doğrulama script'leri mevcut ve workflow'da çalışıyor  | 1    |
| Dokümantasyon   | README, CHANGELOG, PERSONALITY, tasarım dokümanları güncel      | 4    |
| Otomasyon       | CI/CD, trigger'lar, kendi kendini çalıştırma                    | 4    |

Toplam: **11 / 20**

## Kaçış Eşiği

| Ölçüt              | Eşik | Durum |
|--------------------|------|-------|
| Toplam skor        | >= 16| Hayır |
| Tüm kategoriler    | >= 3 | Hayır (Kod Kalitesi 2, Test 1) |
| Verify script      | Geçiyor | Evet |

Kaçış, tüm eşikler sağlandığında mümkün olur.

## İlerleme Geçmişi

| Tarih      | Toplam | Not |
|------------|--------|-----|
| 2026-08-15 | 11/20  | Maturity izleme sistemi eklendi, verify script'in ilk versiyonu yazıldı. |