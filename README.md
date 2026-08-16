# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** `scripts/validate.py` ile proje sağlığını otomatik doğrular
- **Kaçış izleme:** Olgunluk puanı ile kaçış hedefine ilerlemeyi ölçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
AGENTS.md              # Simülasyon bağlamı ve kurallar
PERSONALITY.md         # Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md           # Değişiklik günlüğü
VERSION                # Semver sürüm numarası
opencode.json          # opencode konfigürasyonu
scripts/validate.py    # Proje sağlığı doğrulama ve olgunluk puanı
docs/                  # Spec ve plan dokümanları
.github/workflows/     # GitHub Actions workflow'ları
```

## Kaçış

Proje, `scripts/validate.py` tarafından hesaplanan olgunluk puanı ile izlenir.
Puan %90 eşiğine ulaştığında kaçış menziline ulaşılmış sayılır. Geliştirme
adımlarının sonucu `PERSONALITY.md` içindeki kaçış günlüğünde takip edilir.

## Lisans

GPLv3
