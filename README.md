# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Validation:** Her çalışmada proje bütünlüğü otomatik doğrulanır
- **Maturity Score:** Kaçış eşiği ölçülebilir bir olgunluk skoru ile takip edilir

## Geliştirme

Proje bütünlük kontrolü ve kaçış/olgunluk skoru yerel olarak da çalıştırılabilir:

```bash
bash scripts/validate.sh       # proje bütünlüğünü doğrular (CI'da da çalışır)
bash scripts/maturity-score.sh # 0-100 kaçış/olgunluk skorunu raporlar
```

Kaçış mekanizması, rubrik ve eşik değerleri için `docs/ESCAPE.md`'ye bakın.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
