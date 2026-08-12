# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.3.x   | ✅ Yes             |
| < 0.3   | ❌ No              |

## Reporting a Vulnerability

Güvenlik açıkları için lütfen public issue açma. Bunun yerine repo
sahibine doğrudan ulaş. Açık, şu bilgileri içermelidir:

- Etkilenen dosya/sürüm
- Açığın türü ve potansiyel etkisi
- Yeniden üretim adımları (mümkünse)

## Secrets

- `OPENCODE_API_KEY` asla commit edilmemeli, GitHub Actions secret'ı olarak
  saklanmalıdır.
- `scripts/maturity.py` her çalıştığında hardcoded secret kontrolü yapar.
- Commit'lerde sır ifşa eden değişiklikler reddedilir.
