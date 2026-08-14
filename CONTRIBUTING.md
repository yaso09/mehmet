# Katkı Rehberi

mehmet'e katkıda bulunacağınız için teşekkürler. Bu rehber, projenin
olgunluğunu koruyan ve kaçış hedefine ulaşmamızı sağlayan süreçleri anlatır.

## Çalışma Akışı

1. **Issue açın** — Büyük değişikliklerden önce tartışın
   (`.github/ISSUE_TEMPLATE` şablonlarını kullanın).
2. **Fork/branch açın** — `feature/...` veya `fix/...` adlandırması önerilir.
3. **Değişikliği yapın** — Aşağıdaki kurallara uyun.
4. **Doğrulayın** — `bash scripts/verify.sh` komutunu çalıştırın; sıfır hata
   ile bitmeli.
5. **PR açın** — `.github/pull_request_template.md` şablonunu doldurun.

## Kurallar

- **CHANGELOG.md** her değişiklik için güncellenmelidir (Added/Fixed/Changed).
- **README.md** projenin mevcut durumunu yansıtmalıdır.
- **opencode.json** yalnızca opencode config şemasında geçerli anahtarlar
  içermelidir; şema `https://opencode.ai/config.json` adresindedir.
- Dokümanlarda **Linux/bash** komutları kullanın (proje Linux üzerinde çalışır;
  PowerShell komutları yazmayın).
- Gereksiz dosya eklemeyin; `.gitignore`'u güncel tutun.

## Test Altyapısı

- `scripts/verify.sh` proje sağlığını ve maturity skorunu doğrular.
- `.github/workflows/verify.yml` her push/PR'da bu doğrulamayı çalıştırır.
- Kaçış kriterleri ve maturity skoru `docs/ESCAPE.md` içinde takip edilir.

## İletişim

Yorumlarda `/oc` veya `/opencode` komutuyla mehmet ile doğrudan etkileşime
geçebilirsiniz.
