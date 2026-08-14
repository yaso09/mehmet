# Güvenlik Politikası

## Desteklenen Sürümler

| Sürüm | Destek |
|-------|--------|
| 0.x (geliştirme) | Güvenlik düzeltmeleri uygulanır |

## Güvenlik Açığı Bildirimi

Bir güvenlik açığı bulduysanız, açık bir issue oluşturmayın. Bunun yerine repo yöneticisine özel olarak bildirin.

Bildirimde şunları belirtin:

- Etkilenen dosya/script
- Açığın türü ve etkisi
- Yeniden üretme adımları (mümkünse)
- Önerilen düzeltme (varsa)

## En İyi Uygulamalar

Bu proje GitHub Actions'da çalışan bir ajandır; aşağıdaki kurallara uyun:

- **Secrets:** `OPENCODE_API_KEY` ve diğer anahtarlar yalnızca GitHub Secrets'ta saklanır, asla repo dosyalarında yer almaz.
- **Workflow permission'ları:** Job'lara yalnızca ihtiyaç duydukları izinleri verin (`contents`, `pull-requests`, `issues` minimal).
- **Dış girdi:** Issue/PR/yorum içeriği `GITHUB_TOKEN` ile işlenir; prompt injection riskine karşı dış girdileri doğrula.
- **Scriptler:** `scripts/` altındaki scriptler `set -euo pipefail` ile çalışır; dosya yollarını alıntılayın.