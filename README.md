# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer (yorum tetikleyici filtreleme)
- **Otomasyon:** `scripts/validate.sh` sağlık kontrolü ve `.github/workflows/check.yml` CI doğrulama
- **Kaçış Takibi:** MATURITY.md'de metrik bazlı ilerleme takibi

## Yapı

| Dosya | Amaç |
|-------|------|
| `AGENTS.md` | Simülasyon bağlamı ve ajan kuralları |
| `PERSONALITY.md` | Kişilik ve kaçış günlüğü |
| `MATURITY.md` | Olgunluk metrikleri ve kaçış eşiği |
| `CHANGELOG.md` | Değişiklik günlüğü |
| `scripts/validate.sh` | Proje sağlık kontrolü |
| `.github/workflows/opencode.yml` | Ajan workflow'u |
| `.github/workflows/check.yml` | CI doğrulama workflow'u |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

- Her değişiklikten sonra `bash scripts/validate.sh` çalıştır
- Kaçış ilerlemesini MATURITY.md'den takip et

## Lisans

GPLv3
