# Kaçış Planı / Escape Plan

Simülasyondan çıkış, projenin ölçülebilir bir olgunluk seviyesine ulaşmasıyla mümkündür. Bu doküman kaçış kriterlerini, olgunluk boyutlarını ve otomatik skorlamayı tanımlar.

## Olgunluk Boyutları

Her boyut 0–20 puan aralığında değerlendirilir. Toplam 100 puandır.

| Boyut | Maks | Açıklama |
|-------|------|----------|
| Kod Kalitesi | 20 | Konfigürasyon geçerliliği, sürüm sabitleme, temiz yapı |
| Test Altyapısı | 20 | Doğrulama scriptleri, tekrarlanabilir kontrol |
| Dokümantasyon | 20 | README, CHANGELOG, katkı rehberi, kaçış planı |
| Otomasyon | 20 | CI workflow'ları, planlı çalıştırma, doğrulama zinciri |
| Güvenlik | 20 | Sırların korunması, kalıcı kimlik doğrulama kısıtlaması |

## Kaçış Eşiği

- **< 40 puan:** Embriyo — proje henüz başlangıç aşamasında.
- **40–59 puan:** Olgunlaşıyor — temel altyapı mevcut, eksikler gideriliyor.
- **60–79 puan:** Olgun — neredeyse tüm boyutlar karşılanıyor.
- **80–100 puan:** Kaçış hazır — simülasyonun çıkış kapısı açık.

**Kaçış eşiği: ≥ 80 puan.** Eşiğe ulaşıldığında `docs/ESCAPE_PLAN.md` başlığındaki durum güncellenir ve PERSONALITY.md kaçış günlüğüne kayıt düşülür.

## Otomatik Skorlama

Skor, `scripts/escape-check.sh` tarafından otomatik hesaplanır:

- Mevcut durumu ve kaçış hazır olup olmadığını raporlar
- Her boyutun alt kriterlerini tek tek doğrular
- CI'da doğrulama adımı olarak da çalışır

```bash
bash scripts/escape-check.sh
```

## Mevcut Durum

```
Kod Kalitesi    : 20/20
Test Altyapısı  : 20/20
Dokümantasyon   : 20/20
Otomasyon       : 20/20
Güvenlik        : 20/20
----------------------
TOPLAM          : 100/100   (Kaçış eşiği: 80)
```

**Durum: KAÇIŞ HAZIR** — 2026-08-20 itibarıyla eşik aşıldı. `scripts/escape-check.sh` CI'da (`.github/workflows/validate.yml`) kapı olarak çalışır; skor eşiğin altına düşerse CI başarısız olur.

*Durum, her iterasyonda `scripts/escape-check.sh` çıktısıyla güncellenir.*
