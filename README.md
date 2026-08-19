# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

Güncel sürüm: `0.3.0` (bkz. [VERSION](VERSION))

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her push/PR'da proje bütünlüğü CI'da doğrulanır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

### Doğrulama

Proje bütünlüğü `scripts/validate.py` ile doğrulanır:

```bash
python3 -m pip install pyyaml
python3 scripts/validate.py
```

Doğrulayıcı şunları kontrol eder: zorunlu dosyalar, `opencode.json` geçerliliği,
workflow YAML sözdizimi, `VERSION` ↔ `CHANGELOG.md` ↔ `README.md` tutarlılığı ve
`PERSONALITY.md` kaçış günlüğü. CI'da `.github/workflows/validate.yml` çalışır.

### Sürüm Yönetimi

- `VERSION` dosyası tek kaynaktır (semver `X.Y.Z`)
- Yeni sürüm `CHANGELOG.md`'ye eklenmeli
- Her iterasyon `PERSONALITY.md` kaçış günlüğüne işlenmeli

## Lisans

GPLv3
