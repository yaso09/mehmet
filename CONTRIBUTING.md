# Katkı Rehberi

mehmet'e katkıda bulunmak için:

## Geliştirme Ortamı

- `bash`, `shellcheck`, `jq`, `yq` gerekir
- Tüm scriptler POSIX-uyumlu bash ile yazılmalı ve `shellcheck -x` temiz olmalı

## Testler

```bash
bash scripts/run_tests.sh        # tüm testleri çalıştır
bash scripts/self_assess.sh      # olgunluk skorunu yeniden hesapla
bash scripts/self_assess.sh --check  # eşik kontrolü (kaçış hedefi)
```

Yeni bir test eklemek için `tests/test_*.sh` içinde betik yaz; çalıştırıcı
otomatik olarak bulur. Test başarılıysa `exit 0`, başarısızsa `exit 1` döndür.

## Kurallar

1. Her değişiklik `CHANGELOG.md`'ye eklenmeli
2. `README.md` güncel tutulmalı
3. Olgunluk raporu (`docs/maturity.md`, `docs/maturity.json`) yeniden üretilmeli
4. `shellcheck -x scripts/*.sh tests/*.sh` temiz olmalı
5. CI (`checks` workflow) yeşil olmalı