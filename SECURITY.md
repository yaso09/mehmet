# Güvenlik Politikası

## Desteklenen Sürümler

| Sürüm | Destekleniyor |
|-------|---------------|
| 0.3.x | Evet |
| < 0.3 | Hayır |

## Güvenlik Açığı Bildirimi

Bir güvenlik açığı keşfettiysen lütfen **herkese açık bir issue açma**. Bunun yerine
repo sahibine GitHub üzerinden özel (private) bir güvenlik raporu gönder
(Repositories > Security > Report a vulnerability).

Raporlarda şunları belirt:

1. Etkilenen sürüm/dosya
2. Açığın türü ve etkisi
3. Yeniden üretme adımları
4. Önerilen düzeltme (varsa)

## Önemli Not

Bu proje otonom bir AI ajanı tarafından yönetilir. Workflow içinde kullanılan
`OPENCODE_API_KEY` secret'ı asla commit'lenmemeli veya günlüklere yazılmamalıdır.
Şüpheli bir anahtar sızıntısı fark ederseniz anahtarı hemen GitHub'da yenileyin.
