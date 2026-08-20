# mehmet

Kendi kendini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirir ve kaçış hedefine (olgunluk seviyesi) yönelik somut adımlar atar.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış mekanizması:** Proje olgunluğunu 0-10 arası ağırlıklı skorla ölçer ve eşik değerine ulaşınca kaçışı bildirir

## Kullanım

```bash
pip install -e ".[dev]"

# Testleri çalıştır
python -m pytest

# Olgunluk kontrolü
python -m mehmet .

# JSON çıktı ve özel eşik
python -m mehmet . --json --threshold 9.0

# Makefile üzerinden
make test
make check
```

Olgunluk kriterleri: README, CHANGELOG, PERSONALITY, LICENSE, docs (spec+plan), kaynak paket, test paketi, GitHub Actions, pyproject.toml ve opencode.json. Tümü sağlandığında skor **10.0/10.0** ve kaçış eşiği (varsayılan 8.0) aşılır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3