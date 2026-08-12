# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** `MATURITY.md` üzerinden 100 puanlık kaçış skoru izlenir
- **Doğrulama:** `./scripts/verify.sh` repo sağlığını ve olgunluk skorunu ölçer

## Geliştirme

```bash
# Olgunluk skorunu ve repo sağlığını kontrol et
./scripts/verify.sh

# CI modunda (hata varsa exit code 1)
./scripts/verify.sh --ci
```

Her push/PR'de `.github/workflows/verify.yml` otomatik olarak doğrulama yapar.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
