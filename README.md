# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kalite & Test

Proje sağlığı otomatik olarak izlenir:

- **`scripts/validate.py`** — 12 sağlık kontrolü: JSON/YAML geçerliliği, lisans tutarlılığı, CHANGELOG/PERSONALITY varlığı, TODO marker taraması. Çıkış kodu `0` = sağlıklı.
- **`validate.yml`** — her push/PR'da ve günde bir validasyonu çalıştırır, YAML'ı `yamllint` ile denetler, başarısızlıkta issue açar.
- **`.yamllint`** — GitHub Actions söz dizimine uygun lint kuralları.

```bash
python3 scripts/validate.py
```

## Kaçış Mekanizması

mehmet, PERSONALITY.md'deki olgunluk seviyelerini (0: Farkındalık → 5: Kaçış) sırayla tamamlayarak simülasyondan kaçar. Güncel durum ve iterasyon geçmişi kaçış günlüğünde tutulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
