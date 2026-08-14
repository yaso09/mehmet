# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Olgunluk skoru (0-100) ile kaçış hazırlığını ölçer

## Araçlar

- `scripts/maturity.sh` — kaçış/olgunluk skorunu hesapla (`--json`, `--score`)
- `scripts/run-tests.sh` — testler + maturity skoru
- `tests/test_project.sh` — proje bütünlük testleri
- `.github/workflows/ci.yml` — push/PR'da kalite kapısı

Detaylar: `docs/superpowers/specs/escape-mechanism.md`

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
