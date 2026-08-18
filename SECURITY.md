# Güvenlik Politikası / Security Policy

## Desteklenen Sürümler

| Sürüm | Destek |
|-------|--------|
| 0.3.x | Aktif destek |

## Güvenlik Açığı Bildirimi

Güvenlik açıkları için **public issue açmayın**. Bunun yerine:

1. GitHub'da güvenli özel rapor oluşturun:
   **Security > Report a vulnerability**
2. Raporunuzda:
   - Etkilenen dosyalar/sürümler
   - Açığın açıklaması
   - Olası etki
   - Varsa önerilen düzeltme

## Güvenlik İlkeleri

- `OPENCODE_API_KEY` yalnızca GitHub Secret'ında saklanır, repo'ya yazılmaz.
- `persist-credentials: false` ile checkout yapılır — kalıcı kimlik bilgileri kullanılmaz.
- `.env`, anahtarlar ve loglar `.gitignore` ile dışlanır.
- Üçüncü parti action'lar gerekmedikçe kullanılmaz; kullanılanlar `@v6` gibi pin'li sürümlerdir.