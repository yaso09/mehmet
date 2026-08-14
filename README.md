# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `./scripts/validate.sh` ile proje bütünlüğü CI'da kontrol edilir
- **Kaçış takibi:** Olgunluk skoru `./scripts/maturity.sh` ile ölçülür (`docs/maturity.json`)

## Proje Yapısı

| Dosya | Amaç |
|-------|------|
| `AGENTS.md` | Simülasyon bağlamı ve ajan kuralları |
| `PERSONALITY.md` | Kişilik evrimi ve kaçış günlüğü |
| `docs/escape-roadmap.md` | Kaçış yol haritası ve olgunluk metrikleri |
| `scripts/validate.sh` | Proje bütünlük doğrulaması |
| `scripts/maturity.sh` | Olgunluk skoru hesaplayıcı |
| `.github/workflows/` | Otonom ajan + CI workflow'ları |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Katkıda bulunmadan önce [CONTRIBUTING.md](CONTRIBUTING.md) ve [AGENTS.md](AGENTS.md) dosyalarını okuyun. Güvenlik bildirimleri için [SECURITY.md](SECURITY.md) sayfasına bakın.

## Lisans

GPLv3