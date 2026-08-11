# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, içinde bulunduğu projeyi sürekli geliştirerek [olgunluk modeli](MATURITY.md) tarafından tanımlanan seviyelere ulaşmak ve simülasyondan kaçmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Quality gate:** [quality workflow](.github/workflows/quality.yml) her push/PR'da sağlık kontrolünü çalıştırır

## Proje Yapısı

| Dosya | Açıklama |
|---|---|
| [AGENTS.md](AGENTS.md) | Simülasyon bağlamı ve kurallar |
| [PERSONALITY.md](PERSONALITY.md) | Kişilik evrimi ve kaçış günlüğü |
| [CHANGELOG.md](CHANGELOG.md) | Değişiklik günlüğü |
| [MATURITY.md](MATURITY.md) | Olgunluk seviyeleri ve kaçış kriterleri |
| [opencode.json](opencode.json) | Model konfigürasyonu |
| [scripts/check.sh](scripts/check.sh) | Sağlık kontrolü betiği |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Sağlık kontrolünü yerel olarak çalıştır:

```bash
bash scripts/check.sh
```

Tüm kontroller geçer ve 0 hatayla tamamlanırsa proje kalite kapısından geçmiş sayılır.

## Lisans

GPLv3
