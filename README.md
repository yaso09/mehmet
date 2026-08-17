# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

mehmet, her iterasyonda projeyi tarar, geliştirme fırsatları bulur ve uygular. İlerleme objektif olarak ölçülür:

- **Olgunluk denetimi:** `make maturity` → `scripts/check_maturity.py` projeyi 11 kriter üzerinden puanlar ve kaçış eşiğine (%90) ulaşılıp ulaşılmadığını raporlar
- **Test altyapısı:** `make test` → `tests/test_project.py` repo bütünlüğünü doğrular (AGENTS, CHANGELOG, PERSONALITY, LICENSE, workflow'lar vb.)
- **CI otomasyonu:** `.github/workflows/validate.yml` her push/PR'da testleri ve olgunluk denetimini çalıştırır

Tüm komutlar için: `make validate`

## Lisans

GPLv3
