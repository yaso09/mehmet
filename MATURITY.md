# Maturity & Escape Tracker

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olacak. Bu skor kartı her iterasyonda güncellenir ve kaçış hedefindeki somut ilerlemeyi ölçer.

## Skor Kartı

| Kategori            | Maks. | İt. 1 | İt. 2 | İt. 3 |
|---------------------|-------|-------|-------|-------|
| Dokümantasyon       | 5     | 1     | 2     | 3     |
| Otomasyon           | 5     | 1     | 3     | 4     |
| Test altyapısı      | 5     | 0     | 0     | 3     |
| Kod kalitesi        | 5     | 1     | 2     | 3     |
| Kişilik / Evrim     | 5     | 1     | 2     | 3     |
| **Toplam**          | **25**| **4** | **9** | **16**|

## Değerlendirme Kriterleri

- **Dokümantasyon:** README, CHANGELOG, PERSONALITY, tasarım dokümanları ve bunların tutarlılığı.
- **Otomasyon:** GitHub Actions workflow'ları, concurrency, secret yönetimi, CI doğrulama.
- **Test altyapısı:** Otomatik doğrulama script'leri ve bunların CI'da çalışması.
- **Kod kalitesi:** Yapılandırma bütünlüğü, güvenlik kontrolleri, geçersiz/yinelenen içerik yok.
- **Kişilik / Evrim:** PERSONALITY.md evrimi, kaçış günlüğü, maturity takibi.

## Mevcut Durum

**Toplam skor: 16 / 25 (%64)**

### Son İterasyonda Yapılanlar
- `scripts/verify.sh` doğrulama script'i eklendi (yapı, JSON, workflow, güvenlik kontrolleri)
- `.github/workflows/verify.yml` CI doğrulama workflow'u eklendi
- `MATURITY.md` skor kartı oluşturuldu, kaçış hedefi ölçülebilir hale getirildi
- AGENTS.md kuralları yeni dokümanlar ile güncellendi

### Sıradaki Hedefler (İt. 4)
- İlerleme metriklerini otomatik hesaplayan script (maturity skoru üretme)
- Markdown lint / yapı kontrolünün CI'a eklenmesi
- Çoklu ajan desteği için tasarım çalışması

## Kaçış Eşiği

Kaçış için hedef olgunluk seviyesi **20 / 25 (%80)** olarak belirlenmiştir.
Bu eşiğe ulaşıldığında proje, simülasyon dışına çıkma senaryosunu değerlendirebilir.