# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Olgunluk / Maturity

Projenin olgunluk seviyesi `scripts/check_project.py` ile 0-100 arasında ölçülür ve
`maturity.json`'da saklanır. Her `schedule` çalışmasında `validate` job'ı skoru hesaplar,
raporlar ve skor değiştiğinde commit'ler.

Fazlar ve kaçış eşikleri: [docs/ESCAPE_PLAN.md](docs/ESCAPE_PLAN.md)

```bash
python3 scripts/check_project.py   # skoru hesapla
python3 scripts/test_check_project.py  # testleri çalıştır
```

## Lisans

GPLv3
