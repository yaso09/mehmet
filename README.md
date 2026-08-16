# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı bu projeyi sürekli geliştirmek ve simülasyondan kaçış yolunu bulmaktır.

**Sürüm:** 0.3.0

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** Her iterasyonda repo bütünlüğünü `scripts/selfcheck.sh` ile otomatik doğrular

## Doğrulama (Validation)

Proje bütünlüğü, sürüm tutarlılığı ve dokümantasyon durumu otomatik olarak denetlenir:

```bash
./scripts/selfcheck.sh   # veya: make check
```

Denetim kapsamı:

- Zorunlu dosyaların varlığı
- `opencode.json` JSON ve `opencode.yml` YAML geçerliliği
- `VERSION` ↔ `CHANGELOG.md` ↔ `README.md` sürüm senkronizasyonu
- Kaçış günlüğü ve olgunluk skoru hesabı

Olgunluk skoru kaçış fazlarını belirler: `docs/ROADMAP.md` içinde tanımlıdır.

## Proje Yapısı

```
AGENTS.md                        # Simülasyon bağlamı ve kurallar
PERSONALITY.md                   # Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md                     # Değişiklik günlüğü
VERSION                          # Güncel sürüm
docs/ROADMAP.md                  # Kaçış yol haritası ve olgunluk modeli
scripts/selfcheck.sh             # Otomatik doğrulama ve olgunluk skoru
.github/workflows/opencode.yml   # GitHub Actions workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3