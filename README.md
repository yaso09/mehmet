# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** `scripts/maturity.py` ile proje olgunluk skoru ölçülür; eşik aşıldığında ESCAPE READY durumu tetiklenir

## Geliştirme

```bash
make test        # pytest ile testleri çalıştırır
make maturity    # olgunluk skorunu hesaplar
make check       # test + olgunluk kontrolü
```

## Proje Yapısı

```
AGENTS.md                        # Simülasyon bağlamı ve kuralları
PERSONALITY.md                   # Kişilik ve kaçış günlüğü
CHANGELOG.md                     # Değişiklik günlüğü
opencode.json                    # OpenCode konfigürasyonu
scripts/maturity.py              # Olgunluk skorlama motoru
scripts/maturity_config.json     # Skorlama ağırlıkları ve eşik
tests/test_maturity.py           # Olgunluk testleri
.github/workflows/opencode.yml   # Otonom ajan workflow'u
.github/workflows/ci.yml         # CI (test + olgunluk)
docs/                            # Tasarım dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
