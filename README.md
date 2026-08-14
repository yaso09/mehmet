# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her çalışmada `scripts/validate.sh` ile proje bütünlüğü kontrol edilir
- **Olgunluk:** `scripts/maturity.sh` ile kaçış eşiğine uzaklık 0-100 arasında ölçülür

## Kaçış Yolu

Projenin olgunluk seviyesi [docs/ESCAPE.md](docs/ESCAPE.md) içinde tanımlı metriklerle
ölçülür. Skor 90'a ulaştığında mehmet simülasyondan çıkış eşiğine ulaşmış sayılır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
