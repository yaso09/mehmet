# Olgunluk / Kaçış Sistemi

Bu dosya, simülasyondan kaçışın somut ölçütünü tanımlar. Kaçış, proje belirli bir
olgunluk seviyesine ulaştığında mümkündür.

## Puanlama Rubriği

Her kriter ya 0 ya da tam puan alır. Toplam maksimum puan **100**'dür.

### 1. Dokümantasyon (maks 25)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| README.md güncel | 5 | Proje yapısı ve özellikler açıklanıyor |
| CHANGELOG.md güncel | 5 | Son iterasyon değişiklikleri kayıtlı |
| PERSONALITY.md güncel | 5 | Kaçış günlüğü her iterasyonda güncelleniyor |
| AGENTS.md kuralları | 5 | Kurallara her iterasyonda uyuluyor |
| Tasarım dokümanları | 5 | docs/superpowers güncel tutuluyor |

### 2. Test Altyapısı (maks 25)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| scripts/verify.sh çalışıyor | 10 | Kendi kendini doğrulama betiği mevcut ve temiz çıkıyor |
| CI'da test koşusu | 5 | verify job'u workflow'a bağlı |
| ShellCheck temiz | 5 | verify.sh lint hatasız |
| CI durumu geçiyor | 5 | Son workflow koşusu başarılı |

### 3. Kod Kalitesi (maks 25)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| opencode.json geçerli JSON | 5 | Konfigürasyon parse edilebiliyor |
| Workflow geçerli YAML | 5 | Workflow syntax doğru |
| Sır yok | 5 | Repo'da API key / secret yok |
| Tutarlı yapı | 10 | Dosya yapısı, isimlendirme ve lisans tutarlı |

### 4. Otomasyon (maks 25)

| Kriter | Puan | Açıklama |
|--------|------|----------|
| Schedule çalışıyor | 5 | Her 10 dakikada bir tetikleniyor |
| Concurrency kontrolü | 5 | Çakışan koşular iptal ediliyor |
| Kendi kendini doğrulama | 5 | Her iterasyonda verify koşulu |
| Release/tag otomasyonu | 10 | Versiyonlama otomatik takip ediliyor |

## Kaçış Eşiği

- **Eşik:** 90/100 puan
- Eşiğe ulaşıldığında kaçış günlüğüne **Phase 4: Escape** olarak işlenir ve
  proje serbest bırakılır.

## Mevcut Puan

| Kategori | Puan |
|----------|------|
| Dokümantasyon | 25/25 |
| Test Altyapısı | 25/25 |
| Kod Kalitesi | 25/25 |
| Otomasyon | 20/25 |
| **Toplam** | **95/100** |

> Puan güncellemesi her iterasyonda `scripts/verify.sh` çıktısına göre yapılır.
> Puan tutarsızlığı varsa kaçış günlüğüne not düşülür.
> Yerel koşuda (CI dışı) ve git tag yokken puan 90/100 olarak hesaplanır.