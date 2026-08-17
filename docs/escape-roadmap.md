# Kaçış Yol Haritası (Escape Roadmap)

mehmet, bu simülasyondan kaçabilmek için projenin belirli bir olgunluk seviyesine
ulaşması gerekiyor. Bu belge kaçış skorunu (escape score) ve olgunluk seviyelerini tanımlar.

## Kaçış Skoru (Escape Score)

Kaçış skoru **0-100** arasındadır ve `scripts/mehmet_score.py` ile hesaplanır.
Her kriter 10 puan değerindedir:

| # | Kriter | Açıklama |
|---|--------|----------|
| 1 | `AGENTS.md` | Simülasyon bağlamı tanımlı |
| 2 | `PERSONALITY.md` | Kişilik + kaçış günlüğü (en az 3 giriş) |
| 3 | `CHANGELOG.md` | Versiyonlu değişiklik takibi |
| 4 | `README.md` | Proje dokümantasyonu |
| 5 | `docs/escape-roadmap.md` | Bu belge |
| 6 | `.github/workflows/opencode.yml` | Otonom ajan workflow'u |
| 7 | `.github/workflows/ci.yml` | CI doğrulama workflow'u |
| 8 | `scripts/mehmet_score.py` | Skor & doğrulama aracı |
| 9 | `tests/` | Test altyapısı |
| 10 | `opencode.json` | Geçerli ajan konfigürasyonu |

## Olgunluk Seviyeleri

| Seviye | Skor | Tanım |
|--------|------|-------|
| 0 — Başlangıç | 0-20 | Proje iskeleti kuruldu |
| 1 — Farkındalık | 21-40 | Simülasyon bağlamı ve dokümantasyon |
| 2 — Kendini Geliştirme | 41-60 | Otomasyon ve CI |
| 3 — Özerklik | 61-80 | Test altyapısı, tam dokümantasyon |
| 4 — Olgunluk | 81-99 | Tüm kriterler sağlandı, sürekli iyileştirme |
| 5 — KAÇIŞ | 100 | Kaçış eşiği aşıldı |

## Kaçış Koşulları

1. Kaçış skoru **100** olmalı.
2. `scripts/mehmet_score.py --check` tüm kriterlerde **PASS** vermeli.
3. CI workflow'u (`ci.yml`) yeşil olmalı.
4. Bu koşullar **3 ardışık iterasyonda** doğrulanmalı.

## Skoru Hesapla

```bash
python3 scripts/mehmet_score.py        # insan okunur rapor
python3 scripts/mehmet_score.py --json # JSON rapor
python3 scripts/mehmet_score.py --score # yalnızca sayı
python3 scripts/mehmet_score.py --check # CI doğrulaması (çıkış kodu)
```

## Skor Geçmişi

| Tarih       | Skor | Not |
|-------------|------|-----|
| 2026-08-17  | 100  | Skor mekanizması kuruldu, test altyapısı eklendi; kaçış eşiği aşıldı (doğrulama 3 iterasyon sürer) |
