# Maturity

mehmet'in kaçış hedefi için ölçülebilir olgunluk kriterleri. Skor `scripts/maturity.py` ile hesaplanır ve sonuç `docs/maturity-report.json` dosyasına yazılır.

## Skor Kartı (0-100)

| Kriter | Puan | Açıklama |
|---|---|---|
| AGENTS.md simülasyon prompt'u | 10 | Simülasyon bağlamı ve kuralları mevcut |
| CHANGELOG.md güncel | 10 | Son sürüm girişi son 30 gün içinde |
| PERSONALITY.md kaçış günlüğü | 10 | Son giriş son 60 gün içinde |
| README.md | 10 | Proje tanıtımı mevcut |
| LICENSE | 5 | Lisans dosyası mevcut |
| opencode.json geçerli | 5 | Geçerli JSON |
| GitHub Actions workflow | 10 | `opencode.yml` mevcut |
| Test altyapısı | 20 | `tests/` suite'i başarıyla geçiyor |
| Doğrulama otomasyonu | 10 | `validate.yml` mevcut |
| Olgunluk takibi | 5 | Bu dosya (MATURITY.md) mevcut |
| Kaçış günlüğü derinliği | 5 | En az 3 iterasyon kayıtlı |
| **Toplam** | **100** | |

## Kaçış Eşiği

- **Eşik:** Skor ≥ **80/100**
- **Süreklilik:** Üst üste **3 ardışık çalıştırmada** eşik korunmalıdır
- Sonuç `escape_ready: true/false` olarak raporda kaydedilir

Kaçış, projenin olgunluk eşiğine ulaşmasıyla tetiklenir. Bu eşik kodu değil, süreci ölçer: dokümantasyon, test altyapısı, otomasyon ve sürekli gelişim.

## Rapor

Her çalıştırmada `docs/maturity-report.json` güncellenir:

```json
{
  "score": 80,
  "max": 100,
  "threshold": 80,
  "consistent_runs_required": 3,
  "consistent_runs_above_threshold": 3,
  "escape_ready": true,
  "criteria": { "...": { "label": "...", "points": 10, "earned": 10, "ok": true } },
  "history": [ { "date": "2026-08-16", "score": 80, "max": 100 } ]
}
```

## Çalıştırma

```bash
python3 scripts/maturity.py                 # skoru hesapla, raporu yaz
python3 scripts/maturity.py --fail-below 80 # eşik altıysa exit 1
python3 -m unittest discover -s tests -v    # testleri çalıştır
```