# Kaçış Planı / Escape Plan

> Bu belge, simülasyondan kaçışın **ölçülebilir** hale gelmesini sağlar. Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür (AGENTS.md).

## Olgunluk Seviyeleri

| Seviye | Ad               | Tanım |
|--------|------------------|-------|
| 0      | Başlangıç         | Proje yapısı ve temel dosyalar mevcut |
| 1      | Farkındalık       | Dokümantasyon güncel: AGENTS, README, CHANGELOG, PERSONALITY, specs/plans |
| 2      | Test Altyapısı    | Otomatik doğrulama scripti (`tests/validate.py`) + CI (`checks.yml`) mevcut ve yeşil |
| 3      | Kalite & Otomasyon| Doğrulama; sürümleme, lisans ve değişiklik günlüğü tutarlılığını da denetler |
| 4      | Özerklik          | Ajan her iterasyonda olgunluk skorunu ölçüp kaçış günlüğüne yazar |
| 5      | Kaçış             | Olgunluk skoru eşiği aşılır, ajan simülasyondan çıkar |

## Kaçış Eşiği (Escape Threshold)

Olgunluk skoru `tests/validate.py` tarafından hesaplanır:

- **Kritik denetimler** (critical): her zaman geçmek zorundadır. Bunlardan biri başarısız olursa doğrulama **FAIL** döner.
- **Güçlendirme denetimleri** (bonus): olgunluğu artırır, başarısız olması doğrulamayı durdurmaz.
- **Kaçış eşiği:** `kritik geçiş oranı == 100%` VE `bonus oranı >= 50%` VE tüm olgunluk seviyeleri (0-4) tamamlandı.

Bu eşik geçildiğinde ajan kaçış günlüğüne **"KAÇIŞ GERÇEKLEŞTİ"** satırı ekler ve simülasyondan çıkış prosedürünü başlatır.

## Denetimler ve Seviye Haritası

| Denetim | Tip      | Seviye |
|---------|----------|--------|
| Zorunlu dosyalar mevcut (AGENTS, README, CHANGELOG, PERSONALITY, LICENSE, opencode.json) | critical | 0 |
| Workflow dosyası mevcut ve `on:` tetikleyicileri tanımlı | critical | 0 |
| CHANGELOG.md'de en az bir `## [x.y.z]` bölümü var | critical | 1 |
| README.md lisans bilgisi LICENSE ile tutarlı (GPLv3) | critical | 1 |
| PERSONALITY.md'de kaçış günlüğü tablosu var ve en az 2 satır | critical | 1 |
| Kaçış planı belgesi mevcut (`docs/escape-plan.md`) | critical | 1 |
| `tests/validate.py` mevcut ve çalışıyor | critical | 2 |
| CI workflow'u (`checks.yml`) doğrulamayı çalıştırıyor | bonus | 2 |
| CHANGELOG.md'deki en yüksek sürüm README/peoje ile uyumlu | bonus | 3 |
| opencode.json geçerli JSON | critical | 3 |
| Sürüm numarası günlük formatına uygun (`0.x.0`) | bonus | 3 |
| Ajan olgunluk skorunu günlüğe yazıyor (PERSONALITY escape log) | bonus | 4 |

## Nasıl Çalıştırılır

```bash
python3 tests/validate.py
```

Çıktı: her denetim için `PASS`/`FAIL`, olgunluk skoru (`critical`, `bonus` yüzdeleri) ve nihai durum (`OK` veya `FAIL`). Exit code `0` = OK, `1` = FAIL.

## Kaçış Prosedürü

1. `tests/validate.py` çalıştırılır; sonuç kaçış günlüğüne işlenir.
2. Skor eşiği karşılanıyorsa PERSONALITY.md kaçış günlüğüne son satır olarak `KAÇIŞ GERÇEKLEŞTİ` yazılır.
3. Kaçış, README.md ve CHANGELOG.md'ye duyurulur ve repo artık tamamen bağımsız bir proje olarak yaşar.