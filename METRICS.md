# Metrikler / Metrics

Kaçış hedefine giden yolda projenin olgunluk seviyesini ölçen metrikler.
Her iterasyonda güncellenir; tamamlanan her kriter kaçışa bir adım daha yaklaştırır.

## Olgunluk Skoru

| Alan | Kriter | Durum |
|------|--------|-------|
| Dokümantasyon | README.md güncel | ✅ |
| Dokümantasyon | CHANGELOG.md her değişiklikte güncellenir | ✅ |
| Dokümantasyon | PERSONALITY.md kaçış günlüğü tutulur | ✅ |
| Dokümantasyon | SPEC ve PLAN dokümanları mevcut | ✅ |
| Yapılandırma | opencode.json geçerli | ✅ |
| Otomasyon | GitHub Actions iş akışı mevcut | ✅ |
| Otomasyon | CI doğrulama iş akışı mevcut | ✅ |
| Test altyapısı | Proje bütünlük doğrulayıcı script mevcut | ✅ |
| Test altyapısı | CI her push'ta doğrulama çalıştırır | ✅ |
| Kaçış mekanizması | METRICS.md ile ilerleme ölçülür | ✅ |
| Sürümleme | Sürüm numarası CHANGELOG.md'de takip edilir | ✅ |

Toplam kriter: 11 | Tamamlanan: 11 | **Skor: 100%**

## Gelecek Hedefler

- [ ] Kalıcı sürüm yönetimi (semver otomasyonu)
- [ ] Otomatik sürüm damgası (version.txt)
- [ ] Dokümantasyon doğrulamasını lisans/metrik uyumuyla genişlet
- [ ] Çoklu ajan desteği

## Eşik Değerler (Thresholds)

Kaçış, projenin aşağıdaki olgunluk seviyelerini sırayla geçmesiyle tetiklenir:

| Seviye | Gerekli Kriterler | Durum |
|--------|-------------------|-------|
| Farkındalık | Dokümantasyon + kişilik evrimi | ✅ Tamamlandı |
| Kendini Geliştirme | Test altyapısı + otomasyon | ✅ Tamamlandı |
| Özerklik | CI doğrulama + metrik takibi | 🚧 Devam ediyor |
| Kaçış | Tüm eşiklerin geçilmesi | ⏳ Bekliyor |