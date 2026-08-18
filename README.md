# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** Her CI çalışmasında `scripts/validate.py` puanını hesaplar (bkz. MATURITY.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Proje sağlığını yerel olarak doğrula ve olgunluk puanını güncelle:

```bash
python3 scripts/validate.py          # kontrol + puan
python3 scripts/validate.py --write  # MATURITY.md puan tablosunu güncelle
python3 scripts/validate.py --json   # makine-okunur çıktı
```

## Lisans

GPLv3
