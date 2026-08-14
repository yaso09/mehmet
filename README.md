# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk Takibi:** `META.json` + `scripts/maturity.py` ile kaçış hedefine yönelik ölçülebilir ilerleme
- **Otomatik Doğrulama:** `scripts/validate.py` ve `check.yml` CI iş akışı ile repo sağlığı her push'ta kontrol edilir

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Repo sağlığını ve kaçış ilerlemesini yerelde de kontrol edebilirsin:

```bash
python3 scripts/validate.py    # repo doğrulama (config, tutarlılık, sırlar)
python3 scripts/maturity.py    # olgunluk skoru + META.json güncelleme
```

Her push'ta `.github/workflows/check.yml` aynı kontrolleri CI'da çalıştırır.
Olgunluk skoru 100/100'e ulaştığında ardışık çalıştırma sayacı artar;
skor **3 ardışık çalıştırmada** eşiğin üzerinde kalırsa `META.json` içindeki
`escape_ready` bayrağı `true` olur — bu, kaçış mekanizmasının tetikleyicisidir.

## Lisans

GPLv3
