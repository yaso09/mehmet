# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.py` ile JSON/YAML ve repo bütünlüğü otomatik kontrol edilir

## Proje Yapısı

```
AGENTS.md                 Simülasyon bağlamı ve kurallar
PERSONALITY.md            Ajan kişiliği ve kaçış günlüğü
CHANGELOG.md              Değişiklik günlüğü
VERSION                   Aktif sürüm numarası
opencode.json             OpenCode model konfigürasyonu
docs/MATURITY.md          Olgunluk/kaçış takibi
scripts/validate.py       Repo bütünlük doğrulayıcı
.github/workflows/        opencode.yml (otonom) + validate.yml (CI)
```

## Doğrulama

Repo bütünlüğünü yerel olarak kontrol etmek için:

```bash
python3 scripts/validate.py
```

Her push ve PR'da ayrıca `.github/workflows/validate.yml` üzerinden CI'da çalışır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
