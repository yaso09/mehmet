# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Geliştirme Araçları

- **Sağlık kontrolü:** `python3 scripts/check.py` — repo bütünlüğünü doğrular (zorunlu dosyalar, config şeması, sürüm uyumu, sızıntı tespiti)
- **Testler:** `python3 scripts/test_check.py` — doğrulama mantığının unittest'leri
- **Sürüm artırma:** `python3 scripts/bump_version.py minor` — VERSION + CHANGELOG.md günceller
- **CI:** `.github/workflows/checks.yml` — her push/PR'da kontrol ve testleri koşar

Geliştirme durumu ve kaçış ilerlemesi `AGENTS.md`'deki kaçış kontrol listesinde takip edilir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
