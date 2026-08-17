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

## Proje Yapısı

```
AGENTS.md                          Simülasyon bağlamı ve kurallar
CHANGELOG.md                       Değişiklik günlüğü
PERSONALITY.md                     Kişilik ve kaçış günlüğü
README.md                          Bu dosya
opencode.json                      OpenCode konfigürasyonu
Makefile                           Doğrulama komutları
tests/test_project.py              Proje bütünlük testleri
.github/workflows/                 GitHub Actions workflow'ları
docs/superpowers/                  Tasarım ve uygulama dokümanları
```

## Geliştirme

```bash
make validate   # proje bütünlüğünü doğrular (9 test)
```

Her push ve PR'da `.github/workflows/validate.yml` otomatik çalışır.

## Lisans

GPLv3
