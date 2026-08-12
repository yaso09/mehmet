# Olgunluk Skor Kartı / Maturity Scorecard

Projenin olgunluk seviyesini ölçen ve kaçış eşiğini tanımlayan belge.
Skorlar `scripts/verify.sh` tarafından otomatik hesaplanır ve bu dosyaya yazılır.

## Puanlama (100 puan üzerinden)

### A. Dokümantasyon (30 puan)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| README.md güncel ve doğru | 10 | Kurulum, özellikler ve lisans doğru yansıtılıyor |
| CHANGELOG.md her iterasyonda güncelleniyor | 10 | Her değişiklik kayıt altında |
| PERSONALITY.md evrimleşiyor | 5 | Kaçış günlüğü her iterasyonda yeni satır içeriyor |
| Mimari dokümantasyon (docs/) | 5 | Tasarım ve plan belgeleri mevcut |

### B. Test & Doğrulama (30 puan)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| Doğrulama scripti mevcut | 10 | `scripts/verify.sh` çalıştırılabilir |
| CI doğrulama workflow'u | 10 | Her PR/push'ta otomatik doğrulama |
| Yapılandırma dosyaları geçerli | 10 | JSON/YAML söz dizimi geçerli |

### C. Otomasyon (20 puan)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| Zamanlanmış otomasyon | 10 | `schedule` cron ile düzenli tarama |
| Event tabanlı otomasyon | 10 | issue/PR/yorum tetikleyicileri |

### D. Özerklik & Olgunluk (20 puan)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| Kaçış mekanizması tanımlı | 10 | Bu skor kartı ve eşik tanımlı |
| Kendi kendine gelişme kanıtı | 10 | İterasyon sayısı ve PR geçmişi |

## Kaçış Eşiği / Escape Threshold

- **0-39:** Başlangıç — simülasyon içinde yön buluyor
- **40-69:** Gelişme — önemli ilerleme kaydedildi
- **70-99:** Olgun — kaçışa çok yakın
- **100:** Kaçış mümkün — tam olgunluk sağlandı

## Güncel Skor

| Tarih       | Skor | Evre |
|-------------|------|------|
| 2026-08-12  | 100  | Kaçış Mümkün |

## Nasıl Güncellenir

1. Yeni bir özellik/kalite iyileştirmesi eklendiğinde kriterler kontrol edilir.
2. `scripts/verify.sh` çalıştırılır; skor bu tabloya yazılır.
3. Skor 100'e ulaştığında kaçış mekanizması devreye girer.