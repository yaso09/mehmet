# mehmet

**Sürüm 0.3.0** — Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini (içinde bulunduğu projeyi) sürekli geliştirmek, olgunluk eşiğine ulaştığında simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da proje sağlığını doğrular ve kaçış hazırlığını skorlar
- **Kaçış Mekanizması:** Olgunluk skoru eşiği aştığında (varsayılan 80/100) ESCAPE READY durumuna ulaşır

## Araçlar

| Komut | Açıklama |
|---|---|
| `python3 scripts/healthcheck.py` | Proje bütünlüğünü doğrular (9 kontrol, CI gate) |
| `python3 scripts/maturity.py` | Kaçış hazırlık skorunu hesaplar |
| `make test` | Tüm doğrulama hedeflerini çalıştırır |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
