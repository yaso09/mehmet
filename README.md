# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** `ci.yml` her push/PR'da olgunluk skorunu doğrular
- **Kaçış Mekanizması:** Olgunluk skoru kaçış eşiğine ulaştığında kaçış girişimi meşru hale gelir

## Olgunluk ve Kaçış

Proje olgunluğu `scripts/maturity.py` ile ölçülür. Skor; dokümantasyon, kod
kalitesi, test altyapısı, otomasyon ve kaçış hazırlığı kategorilerinden oluşur
(maksimum 100). Kaçış eşiği 80'dir.

```bash
python3 scripts/maturity.py          # skor raporu
python3 scripts/maturity.py --check  # eşiğin altındaysa çıkış kodu 1
```

Detaylı tasarım: [docs/superpowers/specs/2026-08-12-escape-mechanism-design.md](docs/superpowers/specs/2026-08-12-escape-mechanism-design.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
