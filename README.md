# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Test ve lint kontrolü (`.github/workflows/ci.yml`)
- **Kendi kendini doğrulama:** `tests/` ile proje bütünlüğü sürekli kontrol edilir

## Mimari

```
.github/workflows/opencode.yml   # Otonom ajan (schedule/issue/PR/comment)
.github/workflows/ci.yml         # Test ve lint doğrulaması
tests/test_project.py            # Proje bütünlüğü testleri (17 senaryo)
Makefile                         # test/lint/check hedefleri
AGENTS.md                        # Simülasyon bağlamı ve kurallar
PERSONALITY.md                   # Kişilik, evrim aşamaları ve kaçış günlüğü
CHANGELOG.md                     # Değişiklik günlüğü
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
make test    # testleri çalıştır
make lint    # YAML/JSON doğrula
make check   # test + lint (CI ile aynı)
```

## Lisans

GPLv3
