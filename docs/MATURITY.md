# Maturity Framework

mehmet'in kaçış hedefini somutlaştıran olgunluk çerçevesi. Bu doküman, projenin
hangi olgunluk seviyesinde olduğunu ve kaçış eşiğine ne kadar yaklaştığını tanımlar.

## Kaçış Koşulu (Escape Condition)

Escape, aşağıdaki dört boyutun tamamında belirlenen eşiklere ulaşıldığında mümkündür.
Her boyut 0–100 arasında puanlanır; kaçış için her boyutta en az **70** puan gerekir.

| Boyut | Eşik | Açıklama |
|-------|------|----------|
| Test Altyapısı | 70 | Otomatik doğrulama ve testler çalışıyor |
| Kod Kalitesi | 70 | Temiz, tutarlı ve doğrulanabilir yapı |
| Dokümantasyon | 70 | README, CHANGELOG, mimari dökümanlar güncel |
| Otomasyon | 70 | CI/CD, schedule ve tetikleyiciler çalışır |

## Puan Durumu

> Güncelleme: Her iterasyonda `scripts/check_escape.sh` çalıştırılarak puanlar yenilenir.

| Boyut | Puan | Eşik | Durum |
|-------|------|------|-------|
| Test Altyapısı | 30 | 70 | ⚠️ Geliştiriliyor |
| Kod Kalitesi | 25 | 70 | ⚠️ Geliştiriliyor |
| Dokümantasyon | 40 | 70 | ⚠️ Geliştiriliyor |
| Otomasyon | 45 | 70 | ⚠️ Geliştiriliyor |

## Puanlama Kriterleri

### Test Altyapısı (30/70)
- [x] `scripts/validate.sh` proje sağlık kontrolü
- [ ] GitHub Actions'da otomatik test job'ı
- [ ] Birim test altyapısı (pytest/vitest)
- [ ] Test kapsama raporu
- [ ] Hata durumunda bildirim

### Kod Kalitesi (25/70)
- [x] Tutarlı dosya yapısı
- [x] ShellCheck uyumlu scriptler
- [ ] Kod review checklist
- [ ] API/arayüz sözleşmesi dökümanı
- [ ] Ölçeklenebilir mimari planı

### Dokümantasyon (40/70)
- [x] README.md (kurulum + özellikler)
- [x] CHANGELOG.md (sürüm geçmişi)
- [x] PERSONALITY.md (kişilik + kaçış günlüğü)
- [x] docs/superpowers/ (tasarım + plan)
- [x] docs/MATURITY.md (bu çerçeve)
- [ ] Kullanım kılavuzu / FAQ

### Otomasyon (45/70)
- [x] Schedule (10 dk'da bir)
- [x] Issue/PR/comment tetikleyicileri
- [x] Concurrency kontrolü
- [x] workflow_dispatch (manuel tetikleme)
- [ ] Otomatik versiyonlama / sürüm notları
- [ ] Bağımlılık güncelleme botu
- [ ] Tehdit/risk bildirim otomasyonu

## İterasyon Takibi

Her iterasyonda bu tablo güncellenir ve `scripts/check_escape.sh` çıktısı
PERSONALITY.md'deki kaçış günlüğüne eklenir.