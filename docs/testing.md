# Test Altyapısı

## Çalıştırma

```bash
bash tests/run.sh
```

## Yapı

`tests/run.sh` çalıştırıcısı, `tests/` altındaki tüm `test_*.sh` dosyalarını
sırayla çalıştırır. Herhangi bir test başarısız olursa sıfır olmayan çıkış kodu
döner ve CI durur.

| Test | Açıklama |
|------|----------|
| `test_maturity.sh` | `maturity.sh`'ın 0-100 aralığında skor ürettiğini ve `MATURITY.md` yazdığını doğrular |
| `test_validate.sh` | `validate.sh`'ın temiz bir projede başarıyla geçtiğini doğrular |

## CI Entegrasyonu

`.github/workflows/validate.yml` her push/PR'da şu adımları çalıştırır:

1. `scripts/validate.sh` — proje bütünlüğü doğrulaması
2. `bash tests/run.sh` — test suite
3. `scripts/maturity.sh` — olgunluk skoru güncellemesi

## Yeni Test Ekleme

1. `tests/test_<konu>.sh` adında bir dosya oluştur
2. Script başarısız durumda `exit 1`, başarılı durumda `exit 0` dönsün
3. `chmod +x tests/test_<konu>.sh` ile çalıştırılabilir yap
4. `bash tests/run.sh` ile tüm suite'in geçtiğini doğrula