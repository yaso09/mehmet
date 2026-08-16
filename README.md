# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Mekanizması

mehmet, proje olgunluğunu [MATURITY.md](MATURITY.md) içindeki puanlama
çizelgesiyle ölçer. Toplam puan ≥ 80/100 olduğunda kaçış şartı sağlanmış
sayılır. Güncel durum ve iterasyon geçmişi [PERSONALITY.md](PERSONALITY.md)
kaçış günlüğünde tutulur.

## Doğrulama

Her iterasyon sonunda proje sağlığı otomatik doğrulanır:

```bash
sh scripts/verify.sh   # veya: make verify
```

Kontroller: zorunlu dosyaların varlığı, JSON geçerliliği, lisans tutarlılığı,
sürüm girişleri, kaçış günlüğü ve olgunluk puanı.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
