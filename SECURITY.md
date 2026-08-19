# Güvenlik Politikası

## Desteklenen Sürümler

Bu proje otonom bir ajandır ve tek aktif geliştirme kolu `main`'dir.

## Gizli Anahtar Kullanımı

- `OPENCODE_API_KEY` yalnızca GitHub Secrets'da saklanır, asla repo'ya yazılmaz.
- Repo'da sabit kodlanmış API anahtarı, token veya parola bulunmamalıdır.
- `.env` dosyaları `.gitignore` ile dışlanmıştır.

## Güvenlik Açığı Bildirimi

Güvenlik açığı bulduysanız açık bir GitHub issue oluşturun. Açığın
istismar edilebilir olduğunu düşünüyorsanız lütfen issue'da ayrıntılı
bilgi paylaşmayın, yalnızca varlığını bildirin.

## Otomatik Kontroller

CI workflow'u her çalışmada repo'da gizli anahtar olup olmadığını
`npm run assess` ile tarar (`scripts/assess.mjs` içindeki Güvenlik
kategorisi).