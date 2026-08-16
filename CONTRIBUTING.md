# Katkı Rehberi / Contributing

## Proje Hakkında

**mehmet**, kendi kendisini geliştiren otonom bir AI ajandır. GitHub Actions üzerinde planlı (schedule) olarak çalışır ve her iterasyonda projeyi tarayıp geliştirir.

## Geliştirme Döngüsü

1. `AGENTS.md`'deki simülasyon kurallarını oku.
2. Projeyi tara ve geliştirme fırsatlarını belirle.
3. Değişiklikleri uygula.
4. Her değişikliği `CHANGELOG.md`'ye ekle.
5. `VERSION` dosyasını yükselt ve `CHANGELOG.md`'nin en üst sürümüyle eşleştir.
6. `PERSONALITY.md`'deki kaçış günlüğüne yeni bir satır ekle.
7. `README.md`'yi güncel tut.
8. CI doğrulamalarının geçtiğini doğrula.

## Doğrulama

Değişiklikler şu doğrulamalardan geçmeden tamamlanmış sayılmaz:

- **actionlint** — GitHub Actions workflow sözdizimi
- **markdownlint** — Markdown biçimlendirme (`.markdownlint.json` yapılandırmasıyla)
- **JSON** — `opencode.json` geçerliliği ve beklenen anahtarlar
- **Sürüm tutarlılığı** — `VERSION` ↔ `CHANGELOG.md`

### Yerel Doğrulama

```bash
./scripts/check.sh
```

Bu script CI'ın yaptığı JSON, YAML ve sürüm tutarlılığı kontrollerini çalıştırır.

### Markdown Lint (opsiyonel, yerel)

```bash
npx --yes markdownlint-cli2 --config .markdownlint.json "**/*.md"
```

## Yeni İterasyon Nasıl Hazırlanır

1. `VERSION` dosyasını bir üst sürüme çıkar (ör. `0.3.0` → `0.4.0`).
2. `CHANGELOG.md`'ye `## [0.4.0] - <tarih>` başlığı altında `### Added`, `### Fixed`, `### Changed` bölümlerini ekle.
3. `PERSONALITY.md` kaçış günlüğüne iterasyon numarasını bir artırarak yeni satır ekle.

## Kurallar

- CI doğrulamalarını geçmeyen değişiklik kabul edilmez.
- `CHANGELOG.md` ve `README.md` güncellenmeden iterasyon tamamlanmış sayılmaz.
