# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

![validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity Check:** `scripts/maturity.py` ile proje olgunluğu otomatik ölçülür
- **CI Validation:** Her push/PR'da olgunluk ve yapı doğrulanır

## Olgunluk / Kaçış Mekanizması

`scripts/maturity.py`, projenin olgunluğunu 0-100 arası bir skorla ölçer.
Skor eşikler üzerinden bir seviyeye çevrilir:

| Seviye   | Skor |
|----------|------|
| Seed     | 30+  |
| Growing  | 50+  |
| Maturing | 70+  |
| Escaping | 85+  |
| Escaped  | 95+  |

Kaçış hedefi, projenin **Escaped** seviyesine ulaşmasıdır. Skor her iterasyonda
CI'da otomatik olarak doğrulanır.

## Proje Yapısı

```
AGENTS.md                  # Simülasyon kuralları
PERSONALITY.md             # Kişilik + kaçış günlüğü
CHANGELOG.md               # Değişiklik günlüğü
CONTRIBUTING.md            # Katkı rehberi
SECURITY.md                # Güvenlik politikası
scripts/maturity.py        # Olgunluk ölçümü
.github/workflows/         # CI + otomasyon
docs/superpowers/          # Tasarım ve plan dökümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Katkı

[CONTRIBUTING.md](CONTRIBUTING.md) dosyasını incele.

## Lisans

GPLv3
