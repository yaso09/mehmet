# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![verify](https://github.com/yaso09/mehmet/actions/workflows/verify.yml/badge.svg)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her çalıştığında projeyi tarar, geliştirme fırsatları bulur, uygular ve ilerlemesini belgeler.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** Her iterasyonda `scripts/verify.sh` ile kendi sağlığını doğrular

## Kaçış Durumu

Projenin olgunluk seviyesi `docs/ESCAPE.md` içindeki kontrol listesiyle ölçülür.

| Metrik | Değer |
|--------|-------|
| Maturity skoru | [10/10](docs/ESCAPE.md) |
| CI | [verify](.github/workflows/verify.yml) her push/PR'da çalışır |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Test

Proje sağlığını ve maturity skorunu doğrulamak için:

```bash
bash scripts/verify.sh
```

## Katkı

Katkı süreci için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

## Dokümantasyon

- [Escape Criteria (kaçış kriterleri)](docs/ESCAPE.md)
- [Tasarım dokümanı](docs/superpowers/specs/2026-07-04-mehmet-oz-iyilestiren-ajan-design.md)
- [Değişiklik günlüğü](CHANGELOG.md)
- [Kişilik ve evrim günlüğü](PERSONALITY.md)

## Lisans

GPLv3