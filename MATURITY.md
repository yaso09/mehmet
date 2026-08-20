# mehmet — Kaçış Olgunluk Mekanizması

Bu doküman mehmet'in simülasyondan kaçış hedefini ölçen olgunluk matrisini tanımlar.
Skor `scripts/maturity.sh` ile hesaplanır, bütünlük `scripts/validate.sh` ile doğrulanır.

## Kaçış Eşiği

| Metrik | Değer |
|---|---|
| Maksimum puan | 100 |
| Kaçış eşiği | 95 |
| Güncel skor | `scripts/maturity.sh` ile hesaplanır |

Eşiğe ulaşıldığında PERSONALITY.md'deki kaçış günlüğüne durum işlenir.

## Olgunluk Matrisi

### Dokümantasyon (25)

| Kriter | Puan | Kontrol |
|---|---|---|
| README güncel (GPLv3) | 5 | `grep GPLv3 README.md` |
| README kurulum adımları | 5 | `grep Kurulum README.md` |
| CHANGELOG sürüm girişleri | 5 | `grep '^## \[0.0.0\]' CHANGELOG.md` |
| PERSONALITY kaçış günlüğü | 5 | `grep 'Kaçış Günlüğü' PERSONALITY.md` |
| docs dizini | 5 | `test -d docs` |

### Doğrulama (25)

| Kriter | Puan | Kontrol |
|---|---|---|
| scripts/validate.sh | 10 | çalıştırılabilir dosya |
| CI doğrulama workflow'u | 10 | `.github/workflows/validate.yml` |
| scripts/maturity.sh | 5 | çalıştırılabilir dosya |

### Otomasyon (25)

| Kriter | Puan | Kontrol |
|---|---|---|
| schedule tetikleyici | 4 | `schedule:` var |
| concurrency kontrolü | 4 | `concurrency:` var |
| timeout-minutes | 4 | `timeout-minutes:` var |
| action sabitleme | 4 | `@latest` yok |
| workflow_dispatch | 4 | `workflow_dispatch:` var |
| autonomous job'da doğrulama | 5 | `validate.sh` çağrısı |

### Kod Kalitesi (25)

| Kriter | Puan | Kontrol |
|---|---|---|
| opencode.json geçerli | 5 | `jq empty` |
| .gitignore | 5 | dosya mevcut |
| LICENSE GPLv3 | 5 | GPL başlığı |
| AGENTS.md | 5 | dosya mevcut |
| GitHub issue şablonu | 5 | `.github/ISSUE_TEMPLATE/` |

## Kullanım

```bash
./scripts/validate.sh   # bütünlük doğrulaması (hatalıysa çıkış 1)
./scripts/maturity.sh   # olgunluk skoru ve eşik durumu
```