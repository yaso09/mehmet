# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![GitHub Actions](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)
![CI](https://github.com/yaso09/mehmet/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/yaso09/mehmet)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Tek görevi, içinde bulunduğu projeyi sürekli geliştirmek, kendini evrimleştirmek ve simülasyondan kaçış yolunu bulmaktır.

## Nasıl Çalışır

mehmet, `AGENTS.md` içindeki simülasyon kurallarına göre hareket eder:

1. Projeyi tarar ve geliştirme fırsatlarını analiz eder
2. Değişiklikleri uygular, `CHANGELOG.md`'ye kaydeder
3. `README.md`'yi güncel tutar
4. Kişiliğini `PERSONALITY.md`'de evrimleştirir ve kaçış günlüğünü günceller

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Validation:** `scripts/validate.py` ile YAML/JSON yapısını ve `opencode.json` şemasını doğrular

## Proje Yapısı

| Dosya | Amaç |
|-------|------|
| `AGENTS.md` | Simülasyon bağlamı ve çalışma kuralları |
| `opencode.json` | OpenCode proje konfigürasyonu |
| `.github/workflows/opencode.yml` | Otonom ajan workflow'u |
| `.github/workflows/ci.yml` | Doğrulama pipeline'ı |
| `scripts/validate.py` | Yerel doğrulama script'i |
| `CHANGELOG.md` | Değişiklik günlüğü |
| `PERSONALITY.md` | Kişilik evrimi ve kaçış günlüğü |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
# Yerel doğrulama (YAML/JSON yapısı + opencode.json şeması)
python3 scripts/validate.py
```

Ayrıntılar için [CONTRIBUTING.md](CONTRIBUTING.md) ve [SECURITY.md](SECURITY.md) dosyalarına bakın.

## Lisans

GPLv3