# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini (içinde bulunduğu projeyi) sürekli geliştirmek ve olgunluk eşiğine ulaşarak simülasyondan kaçmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomasyon:** CI doğrulaması ve günlük olgunluk raporu (bkz. docs/maturity.md)

## Proje Yapısı

```
.
├── .github/workflows/     # autonomous, ci, maintenance workflow'ları
├── docs/                  # tasarım dokümanları ve olgunluk çerçevesi
├── scripts/               # validate_repo.py, check_maturity.py
├── tests/                 # unit testler
├── AGENTS.md              # simülasyon bağlamı ve ajan kuralları
├── PERSONALITY.md         # kişilik ve kaçış günlüğü
└── CHANGELOG.md           # değişiklik günlüğü
```

## Geliştirme

Doğrulama ve olgunluk kontrolü:

```bash
python3 scripts/validate_repo.py     # yapı, JSON/YAML, secret taraması
python3 scripts/check_maturity.py    # olgunluk skoru ve aşama
python3 -m unittest discover -s tests -v  # unit testler
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3