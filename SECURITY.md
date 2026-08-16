# Güvenlik Politikası

## Desteklenen Sürümler

| Sürüm | Destekleniyor |
|-------|---------------|
| 0.2.x | Evet |

## Zafiyet Bildirimi

Bir güvenlik zafiyeti bulursan lütfen GitHub üzerinden özel bir **Security Advisory** veya doğrudan issue açarak bildir. Zafiyetleri toplu olarak paylaşma (public disclosure).

## Otomasyon Güvenliği

- `OPENCODE_API_KEY` secret'ı yalnızca GitHub Actions ortamında kullanılır, asla commit edilmez
- Workflow `persist-credentials: false` ile checkout yapar, token sızmaz
- Kapsam (permissions) en az ayrıcalık ilkesiyle tanımlanmıştır
- `.env`, `*.pem`, `*.key` dosyaları `.gitignore` ile hariç tutulur