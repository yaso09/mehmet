# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Olgunluk ve Kaçış Mekanizması

Proje, `scripts/maturity.py` ile hesaplanan **olgunluk skoru** üzerinden kendi
gelişimini izler. Skor 0-100 arasındadır ve beş kategoriye ayrılır:
foundation, automation, documentation, tooling, testing.

- Güncel skor ve ayrıntılı rapor: [docs/status.md](docs/status.md)
- Kaçış eşiği (escape threshold): 80
- `docs/status.md` otomatik üretilir, elle düzenlenmez.

## Geliştirme Araçları

| Komut               | Açıklama                                  |
|---------------------|-------------------------------------------|
| `make validate`     | Yapı/uyumluluk kontrolü (`scripts/validate.py`) |
| `make maturity`     | Olgunluk skoru + `docs/status.md` üretimi |
| `make test`         | Birim testleri (`unittest`)               |
| `make lint`         | GitHub Actions workflow lint (`yamllint`) |
| `make all`          | validate + maturity                       |

`push`/`pull_request` üzerinde tüm bu kontroller
[`.github/workflows/validate.yml`](.github/workflows/validate.yml) CI'ında
otomatik olarak çalışır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Mimari

Tasarım ve uygulama dokümanları `docs/` altındadır:

- [Spec](docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md)
- [Plan](docs/superpowers/plans/2026-07-04-mehmet-implementation.md)

## Lisans

GPLv3
