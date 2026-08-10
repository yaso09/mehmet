# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Verify:** Her push/PR'da `scripts/validate.py` ile proje sağlığını kontrol eder

## Proje Yapısı

```
AGENTS.md                      # Simülasyon bağlamı ve ajan kuralları
PERSONALITY.md                 # Kişilik evrimi, kaçış mekanizması ve günlük
CHANGELOG.md                   # Değişiklik günlüğü
opencode.json                  # OpenCode konfigürasyonu
scripts/validate.py            # Sağlık kontrolü ve olgunluk skorlayıcı
.github/workflows/opencode.yml # Otonom geliştirme workflow'u
.github/workflows/verify.yml   # CI doğrulama workflow'u
docs/                          # Tasarım ve plan belgeleri
```

## Doğrulama ve Olgunluk

`scripts/validate.py` sıfır-bağımlılık bir sağlık kontrolüdür; projenin
AGENTS.md kurallarına uygunluğunu denetler ve kaçış mekanizması için
olgunluk skoru üretir.

```bash
python3 scripts/validate.py        # tüm kontroller + olgunluk skoru
python3 scripts/validate.py --maturity  # sadece skor
python3 scripts/validate.py --json      # makine-okunur çıktı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3