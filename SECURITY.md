# Security

## Güvenlik Duruşu

- `OPENCODE_API_KEY` ve diğer sırlar yalnızca GitHub Secrets'da saklanır.
- Workflow, `persist-credentials: false` ile checkout yapar ve gerektiğinde `GITHUB_TOKEN` kullanır.
- `opencode.json` içinde sır yayınlanmaz; `.env` ve benzeri dosyalar `.gitignore`'dadır.

## Bir Güvenlik Açığı Bildirmek

Bir güvenlik sorunu bulursan, bunu **public issue olarak açma**. Bunun yerine
repo sahibiyle doğrudan iletişime geç. Halka açık PR açmadan önce düzeltmeyi
koordine et.

## En Az Yetki

Workflow'lar yalnızca ihtiyaç duydukları `permissions`'ı tanımlar
(`contents: write`, `issues: write`, `pull-requests: write`, `id-token: write`).