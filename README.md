# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Ölçümü:** `scripts/maturity.py` ile kaçış hedefi puanlanır (`make maturity`)
- **Test Altyapısı:** `tests/` altında ünite testleri (`make test`)
- **Otomasyon:** `Makefile` görevleri ve CI workflow'u

## Geliştirme

```bash
make test       # ünite testlerini çalıştır
make maturity   # kaçış olgunluk puanını göster
make report     # docs/maturity-report.md üret
make check      # test + maturity
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
