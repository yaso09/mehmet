# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** `scripts/self_check.py` ile proje sağlığı ve olgunluk puanı ölçülür (CI'da da çalışır)

## Proje Yapısı

```
AGENTS.md            # Simülasyon bağlamı ve ajan kuralları
PERSONALITY.md       # Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md         # Değişiklik günlüğü
opencode.json        # OpenCode model konfigürasyonu
scripts/self_check.py  # Doğrulama + olgunluk puanlama
.github/workflows/  # opencode.yml (otonom ajan) + validate.yml (CI)
docs/superpowers/   # Tasarım ve uygulama dokümanları
```

## Geliştirme

Otonom ajan dışında CI'da proje bütünlüğü otomatik doğrulanır:

```bash
python3 scripts/self_check.py   # Yerel doğrulama ve olgunluk puanı
```

Her push'ta `.github/workflows/validate.yml` çalışır: dosya bütünlüğü, JSON/YAML sözdizimi ve dokümantasyon tutarlılığı kontrol edilir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
