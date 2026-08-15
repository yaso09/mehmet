# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Projeyi her çalıştığında tarar, geliştirme fırsatları bulur ve kendini iyileştirir.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `make validate` ile proje sağlığını kontrol eder (CI'da otomatik çalışır)

## Mimari

```
GitHub Events ──> opencode.yml ──> OpenCode (DeepSeek V4 Flash Free) ──> Değişiklikler
                                   │
                                   ├── AGENTS.md      (simülasyon kuralları)
                                   ├── PERSONALITY.md (kişilik + kaçış günlüğü)
                                   ├── CHANGELOG.md   (değişiklik geçmişi)
                                   └── METRICS.md     (olgunluk takibi)
```

## Geliştirici Araçları

| Komut | Açıklama |
|-------|----------|
| `make validate` | Proje yapısı, config ve dokümantasyon doğrulaması |
| `make lint` | Workflow YAML lint |
| `make shellcheck` | Shell script statik analizi |
| `make check` | Tüm doğrulama ve lint kontrolleri |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3