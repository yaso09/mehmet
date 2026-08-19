# Katkı Rehberi

mehmet projesine katkıda bulunmak isteyenler için rehber.

## Nasıl Katkıda Bulunulur?

1. Repo'yu fork'la ve `main` üzerinden çalış
2. Yeni bir branch aç (`feature/...` veya `fix/...`)
3. Değişikliklerini yap
4. Testleri çalıştır: `npm test`
5. Olgunluk değerlendirmesini çalıştır: `npm run assess`
6. CHANGELOG.md'ye yeni sürüm satırı ekle
7. PR aç

## Kurallar

- Her değişiklik CHANGELOG.md'ye eklenmeli
- README.md güncel tutulmalı
- Gizli anahtar (secret) asla commit'lenmemeli
- Testler `node --test` ile, bağımlılıksız çalışmalı

## Lisans

Katkılar GPLv3 lisansı altında kabul edilir.