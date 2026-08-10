# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity / Escape:** Kaçış hazırlığını ölçen puanlama sistemi (`mehmet.maturity`)

## Kaçış Sistemi

`mehmet.maturity` modülü, projenin olgunluk seviyesini 8 gösterge üzerinden ölçer ve
kaçış eşiğine ulaşılıp ulaşılmadığını bildirir. Raporu çalıştırmak için:

```bash
python -m mehmet.maturity
```

Eşikler: puan ≥ 90% **ve** PERSONALITY.md kaçış günlüğünde ≥ 3 giriş.

## Geliştirme

Testleri çalıştırmak için:

```bash
pip install pytest
pytest
```

CI, her push/PR'da testleri otomatik çalıştırır ve maturity raporu üretir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
