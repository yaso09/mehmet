# Katkı Rehberi

mehmet'e katkıda bulunmak isteyenler için rehber. Katkılar genellikle agent tarafından otomatik işlenir, ancak insan katkıları da aynı kurallara tabidir.

## Süreç

1. **Scan:** Çalıştırmadan önce projeyi tara ve geliştirme fırsatlarını belirle.
2. **Uygula:** Değişiklikleri AGENTS.md'deki simülasyon kurallarına uygun yap.
3. **Doğrula:** `bash scripts/validate.sh` çalıştır; tüm kontroller geçmeli.
4. **Belgele:**
   - Her değişiklik `CHANGELOG.md`'ye eklenmeli.
   - Gerekirse `README.md` güncellenmeli.
   - Kişilik/kaçış günlüğü `PERSONALITY.md`'ye işlenmeli.

## Kurallar

- Commit'ler yalnızca istek üzerine oluşturulur (agent ortamında otomatik).
- Gizli bilgi (API key vb.) asla commit edilmez.
- Lisans GPLv3'tür; lisans metnini değiştirmeyin.
- Açıkça istenmedikçe yorum eklemeyin.

## Test / Doğrulama

```bash
bash scripts/validate.sh
```

Bu script repo yapısını ve kritik içeriklerin varlığını doğrular. CI'da (`validate` workflow) da otomatik çalışır.

## Kaçış Hedefi

Projenin olgunluk seviyesini artıran her katkı (kod kalitesi, test altyapısı, dokümantasyon, otomasyon) kaçış hedefine yaklaştırır. Bu hedefe yönelik somut adımlar önceliklendirilir.