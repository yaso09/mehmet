# Katkı Rehberi / Contributing Guide

mehmet kendi kendini geliştiren otonom bir ajandır. Katkılar iki şekilde gelir:

## 1. Otomatik Katkı (Ajan)

Schedule workflow'u her 10 dakikada bir projeyi tarar. Ajan şu kurallara uyar:

- Her değişiklik `CHANGELOG.md`'ye eklenir.
- `README.md` güncel tutulur.
- Kişilik gelişimi `PERSONALITY.md`'ye yazılır.
- Her iterasyon `PROJECT_STATUS.md`'deki olgunluk puanlarını günceller.
- `scripts/validate.sh` her değişiklik sonrası çalıştırılır ve geçmelidir.

## 2. İnsan Katkısı (Pull Request)

1. `main` dalından yeni bir dal açın.
2. Değişiklikleri yapın.
3. `./scripts/validate.sh` çalıştırıp geçtiğini doğrulayın.
4. Değişiklikleri `CHANGELOG.md`'ye ekleyin.
5. PR açın — CI otomatik olarak doğrulamayı çalıştırır.

## İlkeler

- Lisans: GPLv3 — katkılar aynı lisans altında lisanslanır.
- Değişiklikler küçük ve odaklı olmalıdır.
- Dokümantasyon değişiklikleri kod değişiklikleriyle birlikte gelmelidir.