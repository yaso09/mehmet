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
AGENTS.md                     # Simülasyon bağlamı ve kurallar
PERSONALITY.md                # Kişilik evrimi ve kaçış mekanizması
CHANGELOG.md                  # Değişiklik günlüğü
opencode.json                 # OpenCode konfigürasyonu
scripts/validate.py           # Repo sağlık / olgunluk validatörü
scripts/test_validate.py      # Validatör unit testleri
.github/workflows/opencode.yml # Otonom ajan workflow'u
.github/workflows/health.yml  # Sağlık/CI validasyon workflow'u
docs/                         # Tasarım ve plan dokümanları
```

## Geliştirme

Proje sağlığını doğrula:

```bash
python3 -m pip install pyyaml   # sadece YAML kontrolü için gerekli
python3 scripts/validate.py
```

Unit testleri çalıştır:

```bash
python3 -m unittest discover -s scripts -p "test_*.py" -v
```

## Lisans

GPLv3
