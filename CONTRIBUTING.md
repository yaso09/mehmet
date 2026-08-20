# Katkı Rehberi / Contributing

mehmet'e katkıda bulunmak için teşekkürler. Bu rehber, katkı sürecini ve
proje kurallarını tanımlar.

## Süreç

1. Değişiklik yapmadan önce mevcut dosyaları okuyun.
2. Tüm değişiklikleri `CHANGELOG.md`'ye ekleyin.
3. Yeni davranış veya araç eklediyseniz `tests/` altına test yazın.
4. Testleri çalıştırın: `python3 -m unittest discover -s tests -v`
5. Olgunluk matrisini doğrulayın: `python3 scripts/maturity.py --check`
6. README'yi güncel tutun.
7. Değişiklikleri ayrı, açıklayıcı commit'lerle yapın.

## Kurallar

- Mevcut kod stiline uyun (bkz. `.editorconfig`).
- Gerekmedikçe yeni bağımlılık eklemeyin; stdlib tercih edin.
- Commit mesajları kısa ve açıklayıcı olsun (örn. `feat:`, `fix:`, `docs:`).
- Değişikliklerinizi özellik dalında (feature branch) yapın ve PR açın.

## Sürüm Yönetimi

Değişiklikler [Semantic Versioning](https://semver.org/) kurallarına göre
`CHANGELOG.md`'de işaretlenir.

## Kaçış / Escape

Bu proje, olgunluk seviyesini `MATURITY.md` üzerinden ölçer. Katkılarınızın
kaçış hedefine uygun olması için:

- Dokümantasyonu güncel tutun.
- Test altyapısını genişletin.
- Otomasyonu güçlendirin.
- `scripts/maturity.py` çıktısının olumsuz etkilenmediğinden emin olun.