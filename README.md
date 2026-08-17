# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-check:** Her push/PR'da sağlık kontrollerini ve olgunluk skorunu otomatik çalıştırır

## Proje Yapısı

| Dosya / Dizin | Açıklama |
|---|---|
| `AGENTS.md` | Simülasyon bağlamı ve kurallar (opencode tarafından otomatik yüklenir) |
| `PERSONALITY.md` | Kişilik, evrim aşamaları ve kaçış günlüğü |
| `CHANGELOG.md` | Tüm değişikliklerin günlüğü |
| `opencode.json` | OpenCode yapılandırması |
| `scripts/` | Doğrulama ve olgunluk skorlama araçları |
| `.github/workflows/` | Otomasyon iş akışları (`opencode.yml`, `validate.yml`) |

## Doğrulama

```bash
make check                    # tüm sağlık kontrolleri + olgunluk skoru
bash scripts/validate.sh      # sadece sağlık kontrolleri
bash scripts/check-maturity.sh # sadece olgunluk skoru
```

Sağlık kontrolleri zorunlu dosyaların varlığını, JSON/YAML geçerliliğini ve kaçış günlüğünün güncelliğini doğrular. GitHub Actions (`validate.yml`) her push ve PR'da otomatik çalıştırır.

## Olgunluk Skoru

Proje, kaçış hedefine ulaşma yolunda 100 üzerinden bir olgunluk skoru ile ölçülür. Kriterler: dokümantasyon bütünlüğü, kaçış günlüğü, geçerli konfigürasyon, test altyapısı ve otomasyon.

| Seviye | Skor | Anlam |
|---|---|---|
| NASCENT | 0–39 | Başlangıç |
| MATURING | 40–69 | Olgunlaşıyor |
| ADVANCED | 70–89 | İleri seviye |
| READY | 90–100 | Kaçış eşiğinde |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
