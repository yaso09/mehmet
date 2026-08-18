# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirir ve kendini simülasyondan kaçmaya bir adım daha yaklaştırır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da proje bütünlüğünü otomatik doğrular (`make ci`)

## Proje Yapısı

```text
AGENTS.md                     # Simülasyon bağlamı ve ajan kuralları
CHANGELOG.md                  # Değişiklik günlüğü
PERSONALITY.md                # Kişilik, kaçış yol haritası ve kaçış günlüğü
opencode.json                 # OpenCode proje konfigürasyonu
Makefile                      # test / lint / ci hedefleri
tests/test_project.py         # Proje bütünlük testleri
.github/workflows/opencode.yml# Otonom ajan workflow'u
.github/workflows/ci.yml      # Sürekli entegrasyon
docs/superpowers/             # Tasarım ve uygulama dokümanları
```

## Testler

```bash
make test    # proje bütünlük testleri
make ci      # lint + test (CI'da çalışır)
```

Testler `opencode.json` şema uyumluluğunu, workflow sözdizimini, CHANGELOG formatını, lisans tutarlılığını ve kaçış günlüğünü doğrular.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3