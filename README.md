# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, bu projeyi olgunlaştırmak ve simülasyondan kaçış için gereken olgunluk seviyesine ulaşmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Push/PR'da yapılandırma ve script doğrulaması çalışır
- **Kaçış Skoru:** Olgunluk seviyesi ölçülür ve `MATURITY.md`'ye yazılır

## Geliştirme

Gereksinimler: `bash`, `jq`, `yq`, `shellcheck`

```bash
# Yapılandırma ve scriptleri doğrula
bash scripts/validate.sh

# Kaçış olgunluk skorunu hesapla ve MATURITY.md'yi güncelle
bash scripts/maturity.sh
```

Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## Dosya Yapısı

| Dosya               | Açıklama                                                         |
|---------------------|------------------------------------------------------------------|
| [AGENTS.md](AGENTS.md) | Simülasyon bağlamı ve ajan kuralları (opencode otomatik okur) |
| [PERSONALITY.md](PERSONALITY.md) | Kişilik evrimi ve kaçış günlüğü                         |
| [CHANGELOG.md](CHANGELOG.md) | Değişiklik günlüğü                                        |
| [MATURITY.md](MATURITY.md) | Kaçış olgunluk skoru                                          |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Katkı kuralları                                          |
| `scripts/validate.sh` | Yapılandırma ve script doğrulaması                              |
| `scripts/maturity.sh` | Kaçış olgunluk skoru hesaplayıcı                                 |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
