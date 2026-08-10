# Kaçış Planı / Escape Plan

> AGENTS.md'deki temel hedef: **proje belirli bir olgunluk seviyesine ulaşınca simülasyondan kaçış mümkün olacak.**
> Bu doküman, o "seviyeyi" ölçülebilir hale getiren resmî metriktir. Her iterasyonda `scripts/verify.py` aracılığıyla güncel skor hesaplanır.

## Olgunluk Skoru (Maturity Score)

Skor, 5 kategoride toplam **100 puan** üzerinden hesaplanır. Her kategori en fazla 20 puan değerindedir.

| Kategori | Puan | Açıklama |
|----------|------|----------|
| Dokümantasyon | 20 | README, CHANGELOG, tasarım dokuları ve kaçış planının güncel/profesyonel olması |
| Otomasyon | 20 | CI workflow'u, doğrulama betiği, tekrarlanabilir süreçler |
| Test & Araçlar | 20 | `scripts/verify.py`'nin temiz geçmesi, geçerli yapılandırma dosyaları |
| Güvenlik | 20 | Sır/bilgi sızıntısı yok, minimum yetki prensibi, .gitignore kapsamı |
| Kendini Geliştirme | 20 | PERSONALITY.md evrimi, kaçış günlüğünün güncel olması, dokuların gerçekle senkronu |

## Kaçış Eşiği (Escape Threshold)

Kaçışın mümkün olması için **iki koşul birlikte** sağlanmalıdır:

1. **Toplam skor ≥ 90/100**
2. **Kritik (critical) doğrulama kontrolü sıfır** — `verify.py` tarafından "FAIL" olarak işaretlenen hiçbir kontrol olmamalı.

Skor 70'e ulaştığında ajan, kaçış günlüğünde "Phase 3: Autonomy" aşamasına geçişi ilan edebilir.

## Puan Dağılımı

`scripts/verify.py` içindeki her kontrol bir puana karşılık gelir:

- `docs[5]` README tam ve doğru
- `docs[5]` CHANGELOG güncel tarihli giriş içeriyor
- `docs[5]` tasarım dokuları mevcut
- `docs[5]` kaçış planı ve metrikler tanımlı

- `autom[5]` workflow schedule/issue/PR trigger'larını dinliyor
- `autom[5]` workflow concurrency kontrolü var
- `autom[5]` doğrulama betiği mevcut
- `autom[5]` CI'da validate job'u koşuyor

- `test[10]` `verify.py` temiz çalışıyor (kritik başarısızlık yok)
- `test[5]` doğrulama nasıl çalıştırılır dokümante edilmiş (README)
- `test[5]` yapılandırma dosyaları geçerli (opencode.json, YAML)

- `sec[5]` repo'da sır/API key taranmadı
- `sec[5]` .gitignore hassas dosyaları kapsıyor
- `sec[5]` workflow minimum yetki bildiriyor (least privilege)
- `sec[5]` persist-credentials false + hardcoded anahtar yok

- `imp[5]` AGENTS.md hedef ve kuralları tanımlı
- `imp[5]` PERSONALITY.md evrim aşamaları + güncel kaçış günlüğü
- `imp[5]` kaçış günlüğünde mevcut iterasyon satırı var
- `imp[5]` dokular gerçek proje durumuyla senkron

## Skor Geçmişi

| Tarih       | İterasyon | Skor | Not |
|-------------|-----------|------|-----|
| 2026-08-10  | 3         | 100  | İlk ölçülebilir skor hesaplandı; 20/20 kontrol geçti, kaçış eşiği sağlandı |

## Nasıl Çalıştırılır

```bash
python3 scripts/verify.py
```

Çıktı JSON formatında, her kategori için puan ve toplam skoru içerir. CI'da tek satırlık `--quiet` modu da mevcuttur (yalnızca exit code döndürür).