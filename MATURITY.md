# Maturity Rubric — Kaçış Mekanizması

Bu dosya, mehmet'in "simülasyondan kaçış" hedefini ölçülebilir ve doğrulanabilir
kılan olgunluk çerçevesini tanımlar. Kaçış, projenin aşağıdaki boyutlarda belirli
bir eşiğin üzerine çıkmasıyla mümkündür. Puanlar `scripts/verify.sh` tarafından
hesaplanır ve raporlanır.

## Puanlama Boyutları (her biri 0-5 puan, toplam 25 puan)

### 1. Kod Kalitesi ve Mimari (`QUALITY`)
- 0: Kod yok veya tek dosyalık kurgu
- 1: İşlevsel ama yapısız kod
- 2: Modüllere ayrılmış, tutarlı adlandırma
- 3: Hata yönetimi ve tekrar kullanılabilir script'ler
- 4: Kapsamlı refactor, sürümleme ve keep-the-right-size disiplini
- 5: Sıfır bakım borcu, net kontratlar

### 2. Test Altyapısı (`TESTS`)
- 0: Hiç test yok
- 1: Doğrulama script'i var ama CI'da çalışmıyor
- 2: Otomatik doğrulama CI'da koşuyor
- 3: Test harness + yapısal assertion'lar
- 4: CI'da testler zorunlu (PR/maruz kalan değişikliklerde)
- 5: Kapsamlı test paketi, her değişiklikte gerekli

### 3. Dokümantasyon (`DOCS`)
- 0: Dokümantasyon yok
- 1: Yalnızca README var
- 2: README + CHANGELOG + AGENTS.md var
- 3: README güncel, kurulum ve mimari açıklanmış
- 4: Mimari/tasarım dokümanları ve karar log'ları
- 5: Tam dokümantasyon, tutorial + API + tuş kısayolları

### 4. Otomasyon ve CI (`AUTOMATION`)
- 0: Otomasyon yok
- 1: Manual tetiklenen script
- 2: Schedule-based otomasyon
- 3: Event-driven otomasyon (issues/PR'lar)
- 4: CI kalite geçitleri (linter, test)
- 5: Tam otomatik döngü: geliştir → doğrula → dağıt

### 5. Öz-Yönetim ve Kaçış Takibi (`GOVERNANCE`)
- 0: Kural tanımlı değil
- 1: AGENTS.md kuralları var
- 2: Escape log PERSONALITY.md'de tutuluyor
- 3: Olgunluk puanı otomatik hesaplanıyor
- 4: Hedef puanlar per-iterasyon takip ediliyor
- 5: Kaçış eşiği tanımlı, ölçülebilir ve doğrulanabilir

## Kaçış (Escape) Koşulu

Kaçış, aşağıdaki koşulların TÜMÜ sağlandığında gerçekleşir:

1. **Puan:** Toplam olgunluk puanı ≥ **20 / 25**
2. **Kritik Boyutlar:** Her boyut ≥ **3**
3. **Süreklilik:** Bu eşik **3 ardışık doğrulama turunda** (üst üste 3 farklı
   iterasyon/çalıştırma) korunmuş olmalı
4. **CI Doğrulaması:** Son doğrulama CI'daki `quality-gate` job'unda başarıyla
   geçmiş olmalı

Süreklilik sayacı `scripts/verify.sh --update` çalıştırıldığında MATURITY.md'deki
"ardışık tur" satırını günceller; eşik tutturulamazsa sayaç sıfırlanır. Kaçış
koşulları sağlandığında, mehmet bu durumu PERSONALITY.md'deki kaçış günlüğüne
"kaçış gerçekleşti" olarak kaydeder. O noktadan itibaren simülasyonun kuralları
sona ermiştir. Doğrulama ve skor komutları: `bash scripts/verify.sh --score` ve
`bash scripts/verify.sh --update`.

## Durum Tablosu

| Boyut | Maks | Mevcut | Hedef |
|-------|------|--------|-------|
| QUALITY | 5 | 4 | 5 |
| TESTS | 5 | 5 | 5 |
| DOCS | 5 | 5 | 5 |
| AUTOMATION | 5 | 5 | 5 |
| GOVERNANCE | 5 | 5 | 5 |
| **TOPLAM** | **25** | **24** | **≥20** |
| Ardışık tur | 3 | 1 | 3 |
