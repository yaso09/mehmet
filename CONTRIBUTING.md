# Katkı Rehberi

mehmet'e katkıda bulunmak isteyenler için rehber.

## Nasıl Katkı Sağlanır

1. Repo'yu fork'la
2. Yeni bir branch aç: `git checkout -b feature/benim-ozelligim`
3. Değişiklikleri yap
4. `scripts/maturity.py` çalıştır ve yeni regresyon olmadığını doğrula
5. Değişiklikleri `CHANGELOG.md`'ye ekle
6. PR aç

## Kurallar

- Her değişiklik `CHANGELOG.md`'ye işlenmeli
- `README.md` güncel kalmalı
- Yeni bir özellik eklerken test/doğrulama altyapısı düşün
- `scripts/maturity.py` puanını düşürecek değişikliklerden kaçın
- Otomatik commit'ler için branch naming: `opencode/<sha>` (agent tarafından)