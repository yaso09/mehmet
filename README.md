# mehmet

![Build](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)
![License](https://img.shields.io/github/license/yaso09/mehmet)
![Olgunluk](https://img.shields.io/badge/olgunluk-95%25-green)

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Quality CI:** Her push'ta proje sağlık kontrolü ve olgunluk skoru hesaplanır

## Olgunluk ve Kaçış

Proje, simülasyondan kaçış hedefine doğru `MATURITY.md` içindeki yol haritasına göre ilerler.

```bash
bash scripts/check_project.sh   # proje yapısını doğrular
bash scripts/maturity.sh        # olgunluk skorunu hesaplar
```

Olgunluk skoru **%80** eşiğine ulaştığında kaçış mekanizması devreye girer. Güncel skor için `MATURITY.md`'deki İlerleme tablosuna bakın.

## Geliştirme

```bash
pip install -r requirements.txt              # bağımlılıklar
ruff check src tests                          # lint
PYTHONPATH=src python -m unittest discover -s tests -v  # testler
bash scripts/check_project.sh                 # sağlık kontrolü
bash scripts/maturity.sh                      # olgunluk skoru
```

## Katkı

Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) ve güvenlik için [SECURITY.md](SECURITY.md) dosyalarına bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
