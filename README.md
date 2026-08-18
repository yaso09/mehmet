# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini (yani bu projeyi) sürekli geliştirmek ve simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Workflow dispatch:** Manuel tetiklemede özel görev prompt'u kabul eder
- **CI sağlık kontrolü:** Her push'ta olgunluk metrikleri doğrulanır

## Mimari

| Bileşen | Görev |
|---|---|
| `AGENTS.md` | Simülasyon bağlamı, kurallar ve kaçış metrikleri |
| `.github/workflows/opencode.yml` | Otonom ajan workflow'u (schedule/issue/PR/comment) |
| `.github/workflows/ci.yml` | Sağlık kontrolü CI'ı (`scripts/check.sh`) |
| `scripts/check.sh` | Olgunluk metriklerini doğrulayan test altyapısı |
| `opencode.json` | OpenCode yapılandırması (model, compaction) |
| `VERSION` / `CHANGELOG.md` | Sürüm takibi |
| `PERSONALITY.md` | Kişilik evrimi ve kaçış günlüğü |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Sağlık kontrollerini çalıştır:

```bash
bash scripts/check.sh
```

Yeni sürüm çıkarırken `VERSION` dosyasını güncelle ve `CHANGELOG.md`'ye tarihli giriş ekle (ör. `## [0.3.0] - YYYY-MM-DD`).

## Lisans

GPLv3