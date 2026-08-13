# Maturity Scorecard

Olgunluk seviyesi, kaçışın (escape) mümkün olduğu ana ölçüttür. Her boyut 0–25 puan üzerinden değerlendirilir. Toplam skor 100 üzerinden hesaplanır. **Kaçış eşiği: 80.**

## Boyutlar

| Boyut | Maks | Açıklama |
|-------|-----:|----------|
| Documentation | 25 | README, docs, CHANGELOG tutarlılığı |
| Test / Validation | 25 | Doğrulama scriptleri, CI |
| Automation | 25 | Makefile, GitHub Actions, otomasyon |
| Code Quality | 25 | Yapı, güvenlik, sürdürülebilirlik |

## Puanlama

### Documentation (25)
- 5: README mevcut ve güncel
- 5: CHANGELOG her iterasyonda güncelleniyor
- 5: docs/ dizininde spec ve plan mevcut
- 5: Persona (PERSONALITY.md) ve escape log güncel
- 5: Lisans ve kurulum dokümantasyonu doğru

### Test / Validation (25)
- 5: Doğrulama scripti mevcut (`scripts/validate.sh`)
- 5: Script tüm kritik dosyaları kontrol ediyor
- 5: JSON/YAML konfigürasyonları doğrulanıyor
- 5: Script deterministik ve hata kodları tanımlı
- 5: CI'da otomatik çalışıyor

### Automation (25)
- 5: Makefile komutları (`make validate`, `make score`)
- 5: GitHub Actions ana workflow (opencode)
- 5: GitHub Actions doğrulama workflow'u
- 5: Concurrency ve güvenli trigger yönetimi
- 5: Manuel/otomatik tetikleme (workflow_dispatch)

### Code Quality (25)
- 5: Sıfır kritik boşluk (TODO/FIXME takibi)
- 5: Konfigürasyonlar geçerli ve tutarlı
- 5: Gizli bilgi yok (secrets/keys)
- 5: .gitignore doğru ve yeterli
- 5: Sürümleme ve değişiklik takibi düzenli

## Skor Takibi

| Tarih       | Doc | Test | Auto | Code | Toplam | Delta | Eşik (80) |
|-------------|----:|-----:|-----:|-----:|-------:|------:|----------:|
| 2026-08-13  | 25  |  25  |  25  | 25   |  100   |  —    |  ✓ GEÇTİ  |

## Kurallar

1. Her iterasyonda bu tabloyu güncelle (yeni satır ekle).
2. Skorlar dürüst ve doğrulanabilir olmalı; `make score` ile tutarlılık kontrol edilir.
3. Toplam ≥ 80 olduğunda kaçış mekanizması tetiklenmeye adaydır.
