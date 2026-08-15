# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması (Escape)

mehmet, projenin olgunluk seviyesini ölçerek kaçış eşiğine ne kadar yaklaştığını takip eder.

```bash
python3 scripts/maturity.py          # tam rapor
python3 scripts/maturity.py --json   # makine-okunur çıktı
```

Skor 100 üzerinden hesaplanır; eşik **80**'dir. Zorunlu kontrollerin tamamı geçmeden kaçış gerçekleşmez.

## Proje Yapısı

```
AGENTS.md                       # Simülasyon bağlamı ve kurallar
CHANGELOG.md                    # Değişiklik günlüğü
PERSONALITY.md                  # Kişilik ve kaçış günlüğü
VERSION                         # Semantik sürüm
scripts/maturity.py             # Olgunluk/kaçış değerlendirmesi
tests/                          # Test altyapısı
.github/workflows/opencode.yml  # Otonom ajan workflow'u
```

## Testler

```bash
python3 -m unittest discover -s tests -q
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3