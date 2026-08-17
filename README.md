# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![mehmet](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)
![validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)
![license](https://img.shields.io/github/license/yaso09/mehmet)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** `scripts/self-check.sh` ile proje sağlığını doğrular
- **CI Validation:** `validate` workflow'u yapılandırma ve syntax kontrolleri yapar

## Proje Yapısı

```
AGENTS.md                      # Simülasyon bağlamı ve ajan kuralları
CHANGELOG.md                   # Değişiklik günlüğü
PERSONALITY.md                 # Kişilik evrimi ve kaçış günlüğü
README.md                      # Bu dosya
opencode.json                  # OpenCode proje konfigürasyonu
LICENSE                        # GPLv3 lisansı
scripts/self-check.sh          # Proje sağlık kontrolü
.github/workflows/opencode.yml # Otonom ajan workflow'u
.github/workflows/validate.yml # CI doğrulama workflow'u
docs/superpowers/              # Tasarım ve uygulama dokümanları
```

## Kalite Kontrol

Proje sağlığını doğrulamak için:

```bash
bash scripts/self-check.sh
```

Bu komut şunları kontrol eder: zorunlu dosyaların varlığı, `opencode.json`'ın
geçerliliği, workflow YAML'larının syntax'ı ve dokümantasyon bütünlüğü.

Her push ve PR'da `validate` workflow'u otomatik olarak çalışır
(`self-check` + `actionlint`).

## Kaçış Skoru

Kaçış hedefi, projenin olgunluk seviyesine ulaşmasıyla mümkündür. Güncel
ilerleme ve ölçütler `PERSONALITY.md` içindeki **Kaçış Skoru** bölümünde
takip edilir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3