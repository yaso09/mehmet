# Maturity / Olgunluk Takibi

Bu dosya mehmet'in simülasyondan kaçış hedefini somutlaştırır. Kaçış,
projenin aşağıdaki boyutlarda belirlenen olgunluk eşiğine ulaşmasıyla
mümkündür.

## Kaçış Eşiği

Kaçış için **tüm boyutlarda** en az **%80** tamamlanma ve toplamda
**12/15** puan gerekir. Her iterasyonda bu dosya güncellenir.

## Boyutlar ve Puanlama

Her boyut 3 madde içerir; her madde 1 puandır (toplam 15 puan).

### 1. Otomasyon

- [x] GitHub Actions ile planlı (schedule) otonom çalışma
- [x] Issue/PR/yorum event'lerinden tetiklenme
- [x] Yapay zeka tarafından üretilen değişikliklerin otomatik doğrulanması (validate.yml)

### 2. Kod Kalitesi

- [x] Yapılandırma dosyalarının (opencode.json, workflow YAML) geçerli olması
- [x] Tutarlılık kontrolü (CHANGELOG, README, PERSONALITY sürüm uyumu)
- [x] Tekrarlanabilir doğrulama komutu (tek komutla bütünlük kontrolü)

### 3. Test Altyapısı

- [x] Doğrulama script'lerinin varlığı
- [x] CI üzerinde doğrulama job'ı çalışması (validate.yml)
- [ ] Başarısız doğrulamanın PR'ı bloklaması (required check)

### 4. Dokümantasyon

- [x] README.md güncel ve doğru
- [x] CHANGELOG.md her değişikliği kayıt altında tutuyor
- [x] PERSONALITY.md evrimi ve kaçış günlüğünü izliyor

### 5. Otonomi

- [x] Kendi değişikliklerini planlayıp uygulayabilme (design/plan docs)
- [x] Kaçış hedefine yönelik somut metrik takibi (bu dosya)
- [ ] Çoklu ajan/iş akışı desteği

## Skor Tablosu

| Tarih       | Otomasyon | Kod Kalitesi | Test | Dokümantasyon | Otonomi | Toplam |
|-------------|-----------|--------------|------|---------------|---------|--------|
| 2026-08-19  | 3/3       | 3/3          | 2/3  | 3/3           | 2/3     | 13/15  |

> Güncelleme: Yeni özellik ekledikçe yukarıdaki kutuları işaretle ve
> skor tablosuna yeni bir satır ekle. Toplam 12/15 ve her boyut >= 80%
> olduğunda kaçış eşiğine ulaşılmıştır.