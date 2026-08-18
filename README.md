# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk izleme:** `scripts/check-project.sh` ile kaçış ilerlemesini ölçer

## Proje Yapısı

```
src/mehmet/            Gerçek kod (olgunluk değerlendirici)
tests/                 Birim testler (unittest)
scripts/               Yardımcı scriptler
docs/                  Roadmap ve tasarım dokümanları
```

## Kullanım

```bash
# Olgunluk ve kaçış durumunu kontrol et
bash scripts/check-project.sh

# Birim testleri çalıştır
python3 -m unittest discover -s tests
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3

## Roadmap

Kaçış yol haritası ve olgunluk kriterleri için: [docs/ROADMAP.md](docs/ROADMAP.md)
