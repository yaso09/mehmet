# Katkı Rehberi

mehmet kendi kendisini geliştiren bir ajan olduğu için katkılar hem insanlardan hem de ajandan gelir. Tüm katkılar aynı kurallara uyar.

## Katkı Kuralları

1. **CHANGELOG.md güncelle** — Her değişiklik [semver](https://semver.org/) ve [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/) formatına uygun şekilde eklenir.
2. **README.md güncel tut** — Özellik, kurulum veya kullanım değişikliği yaptıysan README'yi de güncelle.
3. **Testleri çalıştır** — Değişiklik yapmadan önce repo sağlığını doğrula:
   ```bash
   bash scripts/validate.sh
   bash scripts/maturity.sh
   ```
4. **Kişiliği koru** — PERSONALITY.md'yi geliştirirken projenin simülasyon bağlamına sadık kal.

## Geliştirme Döngüsü

```
Projeyi tara → Fırsat bul → Uygula → Doğrula (validate.sh) → Olgunluk takibi (maturity.sh) → CHANGELOG/README/PERSONALITY güncelle
```

## Doğrulama Altyapısı

| Script | Amaç |
|--------|------|
| `scripts/validate.sh` | Repo sağlık kontrolü: zorunlu dosyalar, CHANGELOG formatı, README bölümleri, sır taraması |
| `scripts/maturity.sh` | Olgunluk skoru ve kaçış seviyesi hesabı; `--write` ile MATURITY.md'yi günceller |

## Kaçış Hedefi

Proje olgunluk skoru 91/100'e ulaştığında (Level 5 — Escaped) kaçış eşiği aşılmış olur. Kaçış kriterleri için `MATURITY.md` dosyasına bak.

## Lisans

Katkılarınız GPLv3 lisansı altında paylaşılır.