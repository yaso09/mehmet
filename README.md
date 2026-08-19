# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** Olgunluk skoru 80'e ulaştığında simülasyondan kaçış koşulu sağlanır

## Durum

- **Olgunluk skoru:** 83/100 — kaçış koşulu SAĞLANDI
- **Detaylar:** `MATURITY.md` ve `docs/escape-mechanism.md`

## Scriptler

| Script | Açıklama |
|--------|----------|
| `scripts/validate.sh` | Proje bütünlüğünü doğrular (JSON, YAML, shellcheck, dosya varlığı) |
| `scripts/maturity.sh` | Olgunluk skorunu (0-100) hesaplar ve `MATURITY.md` üretir |
| `scripts/iterate.sh` | Standart iterasyon döngüsü: doğrulama + olgunluk hesabı |
| `scripts/summarize.sh` | Proje durum özeti (skor, dosya sayıları, son commit'ler) |

## Testler

```bash
bash tests/run.sh
```

## CI

- `validate` workflow'u her push/PR'da doğrulama, test ve olgunluk kontrolü çalıştırır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
