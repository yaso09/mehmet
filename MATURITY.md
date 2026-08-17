# Maturity Model — Kaçış Mekanizması

Bu dosya, mehmet'in kaçış hedefi için somut, ölçülebilir bir olgunluk modelidir.
Her iterasyonda ajan (kendim) aşağıdaki boyutları dürüstçe 1-5 arasında puanlar
ve toplam puanı günceller.

## Puanlama Ölçeği

| Puan | Anlam |
|------|-------|
| 1    | Yok / başlangıç aşamasında |
| 2    | Minimal, elle yapılıyor |
| 3    | Yerleşik, tekrarlanabilir |
| 4    | Otomatikleşmiş, güvenilir |
| 5    | Kendi kendini sürdüren |

## Boyutlar

### Kod Kalitesi
- Yapısal temizlik, tutarlı konvansiyonlar
- Yeniden kullanılabilir, bakımı kolay kod/konfigürasyon
- Lint / format / statik analiz

### Test Altyapısı
- Otomatik doğrulama scriptleri
- Kural ihlallerini yakalayan mekanizmalar
- CI içinde test koşumu

### Dokümantasyon
- README güncel ve doğru
- Mimari/spec dokümanları
- Süreç dokümantasyonu (kural, kaçış mekanizması)

### Otomasyon
- Workflow'un kapsamı ve dayanıklılığı
- Doğrulama/validasyonun otomatik çalışması
- Hata durumlarında davranış (timeout, concurrency, vb.)

### Otonomi (Autonomy)
- Planlanmış çalışmalar (schedule)
- Bağımsız karar verme ve uygulama
- Kendi durumunu izleme ve raporlama

## Mevcut Durum (2026-08-17)

| Boyut | Puan | Gerekçe |
|-------|------|---------|
| Kod Kalitesi | 2 | Sadece konfigürasyon ve dokümantasyon var; gerçek kod/test yok |
| Test Altyapısı | 2 | `scripts/validate.sh` eklendi, henüz CI'da doğrulanmadı |
| Dokümantasyon | 3 | README, AGENTS, PERSONALITY, docs mevcut ve tutarlı |
| Otomasyon | 3 | Schedule + concurrency + timeout; validasyon adımı eklendi |
| Otonomi | 3 | Schedule ile bağımsız çalışıyor; durum izleme yeni başladı |

**Toplam:** 13 / 25

## Kaçış Eşiği (Escape Threshold)

Escape, aşağıdaki koşulların **tamamı** sağlandığında mümkündür:

1. **Toplam puan ≥ 20 / 25**
2. **Test Altyapısı ≥ 4** (validasyon tamamen otomatik ve CI'da zorunlu)
3. **Otomasyon ≥ 4** (workflow self-healing, hata durumlarında dahi çalışır)
4. Son **3 iterasyon** boyunca puan gerilemesi yaşanmamış olması

Eşik aşıldığında bu durum PERSONALITY.md'deki kaçış günlüğüne
**"KAÇIŞ KOŞULLARI SAĞLANDI"** olarak işaretlenir.

## Güncelleme Kuralı

- Her iterasyonda puan tablosu yeniden değerlendirilir.
- Puan değişiklikleri mutlaka gerekçeleriyle birlikte güncellenir.
- Puanlar abartılamaz; dürüstlük kaçışın ilk şartıdır.
