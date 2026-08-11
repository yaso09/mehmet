# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Engine:** Kaçış mekanizmasını ölçülebilir kılan olgunluk puanlama motoru (`mehmet.maturity`)

## Maturity Engine (Kaçış Mekanizması)

`mehmet/maturity.py`, projenin 0..1 arası olgunluk skorunu hesaplar. Skor
altı kategoriden oluşur: docs (%20), changelog (%15), tests (%25),
automation (%20), hygiene (%10), escape-log (%10). `0.8` ve üzeri
`ESCAPE_READY` olarak kabul edilir.

```bash
python -m mehmet.maturity .          # detaylı rapor
python -m mehmet.maturity . --status-only   # sadece durum
```

Testleri çalıştırmak için:

```bash
python -m unittest discover -s tests -v
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
