# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Mimari

```
.github/workflows/
├── opencode.yml   # ana ajan workflow'u (schedule / issue / PR / comment)
└── ci.yml         # her push/PR'da self-check + test + actionlint
scripts/
└── self_check.py  # proje sağlığını doğrulayan bağımsız araç
tests/
└── test_self_check.py  # self_check için unittest testleri
```

## Geliştirme

```bash
make check   # proje self-check'ini çalıştırır
make test    # unit testleri çalıştırır
```

`self_check.py` AGENTS.md kurallarını makinelere denetletir: CHANGELOG bakımı,
README güncelliği, kaçış günlüğü ve yapılandırma bütünlüğü. CI hattı her
değişiklikte bunları otomatik doğrular.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
