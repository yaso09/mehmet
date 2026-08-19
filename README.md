# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kendi kendini doğrulama:** `make validate` ile test + sağlık kontrolü + YAML doğrulama

## Proje Yapısı

```
AGENTS.md                        # Simülasyon bağlamı ve ajan kuralları
PERSONALITY.md                   # Kişilik evrimi ve kaçış günlüğü
scripts/repo_health.py           # Repo sağlık kontrol aracı
scripts/validate_workflows.py    # Workflow YAML doğrulayıcı
tests/test_repo_health.py        # Unit testler
.github/workflows/opencode.yml   # Ana ajan workflow'u
.github/workflows/ci.yml         # CI (test + kontrol + YAML)
Makefile                         # test / check / yaml / validate
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
make test      # unit testleri çalıştır
make check     # repo sağlık kontrolü
make yaml      # workflow YAML doğrula
make validate  # hepsi
```

## Lisans

GPLv3
