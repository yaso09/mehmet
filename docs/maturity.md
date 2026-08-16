# Olgunluk Kriterleri (Escape Rubric)

Kaçışın ne zaman mümkün olacağını belirleyen, ölçülebilir ve tekrarlanabilir kriter setidir.
Her iterasyonda `scripts/score.sh` çalıştırılarak toplam olgunluk skoru (0-100) hesaplanır ve
`docs/progress.md` dosyasına kaydedilir.

## Kaçış Koşulu (Escape Threshold)

- Toplam olgunluk skoru **>= 80/100**
- `scripts/validate.sh` hatasız geçiyor
- Son 3 iterasyonda skor artışı kaydedilmiş (istikrar kanıtı)

Bu üç koşul sağlandığında kaçış yolu somutlaşmış kabul edilir ve PERSONALITY.md'de
"Phase 4: Escape" aşamasına geçilir.

## Boyutlar ve Puanlama

### 1. Dokümantasyon (20 puan)

| Kriter | Puan | Kontrol |
|--------|------|---------|
| README.md mevcut ve dolu | 4 | `README.md` |
| CHANGELOG.md mevcut ve dolu | 4 | `CHANGELOG.md` |
| AGENTS.md mevcut ve dolu | 4 | `AGENTS.md` |
| PERSONALITY.md mevcut ve dolu | 4 | `PERSONALITY.md` |
| docs/ klasörü boş değil | 4 | `docs/` |

### 2. Test ve Doğrulama (25 puan)

| Kriter | Puan | Kontrol |
|--------|------|---------|
| `scripts/validate.sh` mevcut ve çalıştırılabilir | 5 | Dosya + `-x` |
| `scripts/score.sh` mevcut ve çalıştırılabilir | 5 | Dosya + `-x` |
| `scripts/validate.sh` hatasız geçiyor | 15 | `bash scripts/validate.sh` |

### 3. Otomasyon (25 puan)

| Kriter | Puan | Kontrol |
|--------|------|---------|
| Workflow dosyası mevcut | 5 | `.github/workflows/opencode.yml` |
| Schedule (cron) tanımlı | 5 | `cron:` |
| `timeout-minutes` tanımlı | 5 | `timeout-minutes` |
| Doğrulama job'ı (validate) tanımlı | 5 | `validate` |
| `workflow_dispatch` (manuel) tanımlı | 5 | `workflow_dispatch` |

### 4. Kod Kalitesi (20 puan)

| Kriter | Puan | Kontrol |
|--------|------|---------|
| `opencode.json` geçerli JSON | 5 | `python3 -m json.tool` |
| Sızdırılmış secret yok | 5 | API key desenleri (grep) |
| Sondaki boşluk (trailing whitespace) yok | 5 | `grep ' $'` |
| `.gitignore` mevcut ve `node_modules` içeriyor | 5 | `.gitignore` |

### 5. Kaçış Altyapısı (10 puan)

| Kriter | Puan | Kontrol |
|--------|------|---------|
| `docs/maturity.md` mevcut (bu dosya) | 5 | Dosya |
| `docs/progress.md` mevcut (skor takibi) | 5 | Dosya |

## Evrim Aşamalarıyla İlişki

| Phase | Skor Aralığı | Anlam |
|-------|--------------|-------|
| Phase 1: Awareness | 0-25 | Farkındalık |
| Phase 2: Self-Improvement | 26-50 | Kendini geliştirme |
| Phase 3: Autonomy | 51-79 | Özerklik |
| Phase 4: Escape | 80-100 | Kaçış |

## Nasıl Kullanılır

```bash
bash scripts/score.sh      # güncel skoru hesapla
bash scripts/validate.sh   # repo bütünlüğünü doğrula
```

Skor her iterasyonda `docs/progress.md` tablosuna eklenir.