# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Kontrolü:** `scripts/healthcheck.py` her çalıştırmada proje olgunluğunu ölçer

## Olgunluk ve Kaçış

Proje, [MATURITY.md](MATURITY.md) içindeki ölçülebilir kriterlerle takip edilen
bir olgunluk seviyesine sahiptir. Her iterasyonda `scripts/healthcheck.py`
çalıştırılır ve skor güncellenir. Kaçış, tüm kriterler yerine getirildiğinde
(`python3 scripts/healthcheck.py --strict` temiz geçtiğinde) mümkün olacaktır.

```bash
python3 scripts/healthcheck.py          # skor ve rapor
python3 scripts/healthcheck.py --strict # kaçış kriterlerini doğrula
python3 scripts/healthcheck.py --json   # makine tarafından okunabilir çıktı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
