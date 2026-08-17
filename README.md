# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
AGENTS.md                        Simülasyon bağlamı ve kurallar
MATURITY.md                      Olgunluk/kaçış eşiği ve metrikler
PERSONALITY.md                   Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md                     Değişiklik günlüğü
opencode.json                    OpenCode konfigürasyonu
.github/workflows/opencode.yml   Ana otomasyon workflow'u
.github/workflows/ci.yml         CI doğrulama workflow'u
docs/                            Tasarım ve plan dokümanları
scripts/maturity.py              Olgunluk skoru hesaplama aracı
tests/                           Proje doğrulama testleri
```

## Testler ve Olgunluk

```bash
python3 -m unittest discover -s tests   # testleri çalıştır
python3 scripts/maturity.py             # olgunluk skorunu gör
```

Kaçış eşiği **80/100**'dür. Detaylar için [MATURITY.md](MATURITY.md).

## Lisans

GPLv3
