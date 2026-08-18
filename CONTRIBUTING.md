# Contributing

mehmet'e katkıda bulunmak için aşağıdaki kurallara uy.

## Geliştirme Ortamı

Gereksinimler:

- `bash` 4+
- `jq` (JSON doğrulama)
- `yq` (YAML doğrulama)
- `shellcheck` (script denetimi)

## Doğrulama

Değişiklik yapmadan önce ve sonra her zaman doğrulama scriptini çalıştır:

```bash
bash scripts/validate.sh
```

Kaçış olgunluk skorunu görmek için:

```bash
bash scripts/maturity.sh
```

## Kurallar

1. Her değişiklik `CHANGELOG.md`'ye `### Added` / `### Changed` / `### Fixed` olarak eklenir.
2. `README.md` güncel tutulur.
3. `PERSONALITY.md`'deki kaçış günlüğüne her iterasyonda yeni satır eklenir.
4. Scriptlerde `shellcheck` hatasız olmalıdır.
5. Yeni dosya eklerken `.editorconfig` kurallarına uyulur.
