# Olgunluk Seviyeleri (Maturity Levels)

Bu belge, mehmet'in simülasyondan kaçışı için gereken olgunluk seviyesini tanımlar.

## Ölçüm

`scripts/maturity.sh` projeyi 12 kriter üzerinden skorlar:

| Kategori  | Kriter                              |
|-----------|-------------------------------------|
| Temel     | AGENTS.md mevcut ve dolu            |
| Temel     | CHANGELOG.md mevcut ve dolu         |
| Temel     | README.md mevcut ve dolu            |
| Temel     | PERSONALITY.md mevcut ve dolu       |
| Temel     | LICENSE mevcut                      |
| Temel     | .gitignore mevcut                   |
| Yapılandırma | opencode.json geçerli JSON        |
| Yapılandırma | Workflow'da validate job'u var    |
| Dokümantasyon | docs/ klasörü dolu                 |
| Dokümantasyon | MATURITY.md mevcut                 |
| Kalite     | Test altyapısı mevcut               |
| Kalite     | Testler başarılı                    |

## Seviyeler

- **Level 1 — Foundation (0–5):** Proje yapısı oluşmuş, temel dokümantasyon mevcut.
- **Level 2 — Quality (6–8):** Yapılandırma ve dokümantasyon doğrulanabilir durumda.
- **Level 3 — Automation (9–10):** Test altyapısı ve CI doğrulaması aktif.
- **Level 4 — Escape (11–12):** Olgunluk eşiği aşıldı; kaçış hazır.

## Kaçış Eşiği

Kaçış eşiği: **11 / 12**. Bu eşiğe ulaşıldığında `scripts/maturity.sh --check` başarıyla döner.

```bash
bash scripts/maturity.sh --check
```

Eşik, `ESCAPE_THRESHOLD` ortam değişkeniyle geçici olarak değiştirilebilir.

## Hedef

Her iterasyonda skoru artırmak ve kayıt altına almak. Skorlar CHANGELOG.md'de takip edilir.