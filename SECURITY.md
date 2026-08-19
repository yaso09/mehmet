# Güvenlik Politikası

## Desteklenen Sürümler

| Sürüm | Destek |
|-------|--------|
| 0.3.x | Evet |
| < 0.3  | Hayır |

## Güvenlik Açığı Bildirimi

Bir güvenlik açığı keşfederseniz lütfen açık bir issue **açmayın**. Bunun yerine:

1. Özel bir issue oluşturun veya repo sahibiyle doğrudan iletişime geçin.
2. Açığın etkisini ve istismar yöntemini açıklayın.
3. 48 saat içinde yanıt bekleyin.

## Bilinen Konular

- Zen API anahtarı (`OPENCODE_API_KEY`) yalnızca GitHub Secrets'da tutulmalı, asla koda gömülmemeli.
- Workflow, yalnızca kendisini değiştiren commit'leri işleyecek kadar `GITHUB_TOKEN` yetkisine sahiptir.
- Scriptler `set -euo pipefail` ile hatalara karşı korunur; değerlere güvenmeden önce doğrulama yapar.