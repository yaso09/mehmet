# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Geliştirme Araçları

Proje, kaçış hedefini ölçülebilir kılan bir araç seti içerir:

- **Olgunluk değerlendirmesi:** `python3 scripts/assess.py` projeyi beş boyutta
  (dokümantasyon, değişiklik takibi, otomasyon, test, kod kalitesi) 0-100 ölçer.
- **Birim testleri:** `python3 -m unittest discover -s tests` tüm testleri çalıştırır.
- **Otomatik doğrulama:** `.github/workflows/validate.yml` her push/PR'da
  skoru, testleri ve workflow YAML'ını kontrol eder.
- **Kaçış dokümanı:** `docs/ESCAPE.md` olgunluk eşiklerini ve kaçış protokolünü tarif eder.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
