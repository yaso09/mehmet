# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Kontrolü:** `scripts/health-check.sh` ile proje bütünlüğünü ve olgunluk skorunu doğrular (CI'da otomatik çalışır)

## Sağlık Kontrolü

Projenin bütünlüğünü doğrulamak ve olgunluk skorunu hesaplamak için:

```bash
bash scripts/health-check.sh        # detaylı rapor
bash scripts/health-check.sh --json # CI için JSON çıktı
```

Kontrol edilenler: zorunlu dosyalar, CHANGELOG.md/README.md/PERSONALITY.md tutarlılığı, kaçış günlüğü, opencode.json geçerliliği, workflow yapısı, TODO/FIXME kalıntıları ve olgunluk yüzdesi. Kritik hata varsa çıkış kodu `1` olur ve CI işi başarısız olur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
