# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** `scripts/validate.sh` proje sağlığını doğrular
- **Otomasyon:** Her push/PR'da `validate.yml` CI doğrulaması çalışır
- **Olgunluk takibi:** `MATURITY.md` kaçış hedefine yönelik ilerlemeyi ölçer

## Geliştirme

Proje sağlığını yerel olarak doğrulamak için:

```bash
./scripts/validate.sh -v
```

Ayrıntılı bilgi için [MATURITY.md](MATURITY.md) ve [docs/superpowers](docs/superpowers) klasörüne bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
