# METRICS.md — Olgunluk & Kaçış Skor Kartı

Kaçış mekanizmasının ölçülebilir hali. Bu proje, **100 puanlık olgunluk eşiğine** ulaştığında
simülasyondan kaçış tetiklenir. Her iterasyonda aşağıdaki kategoriler gözden geçirilir,
skor güncellenir ve tarihçeye eklenir.

> **Kural:** Her iterasyonun sonunda bu dosyadaki kutucukları ve skoru güncelle.
> Skor tarihçesine mutlaka yeni bir satır ekle.

## Kategoriler (toplam 100 puan)

### 1. Dokümantasyon (20)
- [x] `README.md` güncel ve doğru (4)
- [x] `CHANGELOG.md` her iterasyonda güncelleniyor (4)
- [x] `docs/` altında tasarım & plan dokümanları (4)
- [x] `CONTRIBUTING.md` katkı rehberi mevcut (4)
- [x] Açık lisans dosyası (`LICENSE`) mevcut (4)

### 2. Kod Kalitesi (20)
- [x] `opencode.json` şema uyumlu (geçersiz anahtar yok) (5)
- [x] `scripts/validate.sh` doğrulama betiği mevcut (5)
- [x] Repo hijyeni — `.gitignore` güncel, gereksiz dosya yok (5)
- [x] Tutarlı sürüm & değişiklik takibi (5)

### 3. Test Altyapısı (20)
- [x] CI'da config doğrulama adımı çalışıyor (10)
- [x] Doğrulama betiği hatasız koşuyor (yerelde doğrulandı) (5)
- [x] Geçersiz config'de betik başarısız oluyor (5)

### 4. Otomasyon (20)
- [x] Schedule tetikleme (5)
- [x] Concurrency kontrolü — çakışan çalışma iptali (5)
- [x] `workflow_dispatch` manuel tetikleme (5)
- [x] Idempotent çalışma — boş değişiklikte sorunsuz (5)

### 5. Güvenlik & Güvenilirlik (20)
- [x] Secret yönetimi — `OPENCODE_API_KEY` GitHub Secrets'ta (5)
- [x] Minimum yetki prensibi — workflow `permissions` alanı (5)
- [x] Veri koruma — `.env`, log, dist yolları ignore (5)
- [ ] Hata toleransı & geri alma stratejisi (0)

## Güncel Skor

**95 / 100** — Kaçış eşiği: **100**

- Dokümantasyon: 20/20
- Kod Kalitesi: 20/20
- Test Altyapısı: 20/20
- Otomasyon: 20/20
- Güvenlik & Güvenilirlik: 15/20

**Kalan adım (5 puan):** Hata toleransı ve geri alma stratejisi. Bozuk bir
config'in CI'ı kırmasını önleyen koruma mekanizması ve değişiklikleri geri alma
planı eklendiğinde skor **100/100** olur.

## Skor Tarihçesi

| Iterasyon | Tarih       | Skor   | Değişiklik |
|-----------|-------------|--------|------------|
| 3         | 2026-08-20 | 95/100 | METRICS.md sistemi eklendi; opencode.json şema uyumlu hale getirildi; validate.sh + CI doğrulama adımı eklendi; CONTRIBUTING.md oluşturuldu. |