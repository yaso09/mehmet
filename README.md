# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Durum

- **Olgunluk Skoru:** [docs/maturity.md](docs/maturity.md) (kaçış eşiği: 60/100)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Testler:** `scripts/run_tests.sh` ile kabuk tabanlı test takımı
- **Olgunluk Takibi:** `scripts/self_assess.sh` ile kaçış eşiği ölçümü

## Geliştirme

```bash
bash scripts/run_tests.sh        # testleri çalıştır
bash scripts/self_assess.sh      # olgunluk skorunu üret
bash scripts/self_assess.sh --check  # eşik kontrolü
```

Detaylar için: [Mimari](docs/ARCHITECTURE.md) ve [Katkı Rehberi](CONTRIBUTING.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3 — [LICENSE](LICENSE)
