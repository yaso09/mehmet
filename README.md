# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** [MATURITY.md](MATURITY.md) ile ölçülebilir olgunluk eşiği
- **Test Altyapısı:** [scripts/](scripts/) altında repo sağlık doğrulaması ve olgunluk skorlama

## Mimari

- [AGENTS.md](AGENTS.md) — Simülasyon bağlamı ve çalışma kuralları
- [PERSONALITY.md](PERSONALITY.md) — Kişilik evrimi ve kaçış günlüğü
- [MATURITY.md](MATURITY.md) — Kaçış eşiği ve olgunluk boyutları
- [CHANGELOG.md](CHANGELOG.md) — Değişiklik günlüğü
- [docs/superpowers](docs/superpowers/) — Tasarım dokümanları ve uygulama planları

## Scriptler

| Script | Açıklama |
|--------|----------|
| `scripts/validate.sh` | Repo bütünlüğünü kontrol eder (JSON/YAML, çakışma işaretçileri, sırlar, sözdizimi) |
| `scripts/maturity-score.sh` | Olgunluk skorunu hesaplar; `--update` ile MATURITY.md tablosunu günceller |

Her PR'da `.github/workflows/validate.yml` bu scriptleri çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3