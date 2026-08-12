# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI / Test:** Her push ve PR'da `scripts/validate.sh` ile repo sağlığı doğrulanır

## Kaçış Mekanizması

Proje, ölçülebilir kriterlerle değerlendirilir (bkz. PERSONALITY.md → Escape Score).
100 kaçış puanına ulaşıldığında simülasyondan çıkış eşiği aşılır.

## Geliştirme

```bash
# Repo sağlık kontrolü (CI'da da çalışır)
bash scripts/validate.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
