# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Sistemi:** `MATURITY.md` ile kaçış mekanizması (skor ≥ 90/100)
- **CI Doğrulama:** `scripts/check-repo.sh` her push'ta repo sağlığını ve olgunluk skorunu ölçer

## Olgunluk ve Kaçış

Kaçış kriterleri `MATURITY.md`'de tanımlıdır. Skoru yerel olarak hesaplamak için:

```bash
bash scripts/check-repo.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
