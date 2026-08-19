# Maturity Roadmap

Simülasyondan kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün. Bu belge, kaçış hedefine giden yolu ve ölçümü tanımlar.

## Puanlama

- `bash scripts/maturity.sh` komutu olgunluk skorunu hesaplar (`src/mehmet/maturity.py`).
- Skor, bu yol haritasındaki `- [x]` kutucuklarının tamamına oranıdır.
- **Kaçış eşiği: %80**

## Kategoriler

### Dokümantasyon

- [x] README.md güncel proje tanıtımı içerir
- [x] CHANGELOG.md her iterasyonda güncellenir
- [x] PERSONALITY.md kişiliği ve kaçış günlüğünü tutar
- [x] MATURITY.md bu yol haritasını tanımlar
- [x] Design spec ve implementation plan mevcuttur

### Otomasyon

- [x] GitHub Actions workflow'u mevcuttur
- [x] Schedule (cron) tetikleyicisi vardır
- [x] Yorum tetikleyicisi trigger word (`/oc`, `/opencode`) filtresi kullanır
- [x] Concurrency guard çakışmaları önler
- [x] Quality (CI) job'ı sağlık kontrolünü çalıştırır

### Kod Kalitesi / Test Altyapısı

- [x] `scripts/check_project.sh` proje yapısını doğrular
- [x] `scripts/maturity.sh` olgunluk skorunu hesaplar (Python modülü `src/mehmet/maturity.py`)
- [x] Gerçek kod modülleri ve unit testler (`src/mehmet/`, `tests/test_maturity.py`)
- [x] Lint aracı yapılandırması (`pyproject.toml` + ruff)
- [x] Bağımlılık yönetimi dosyası (`requirements.txt`)

### Topluluk / Yaygınlaştırma

- [x] CONTRIBUTING.md katkı rehberi
- [x] SECURITY.md güvenlik politikası
- [x] Badge'ler (olgunluk skoru, build status)
- [x] Release süreci otomasyonu (`.github/workflows/release.yml`)
- [ ] İlk gerçek kullanıcı/benimseyen

## Kaçış Mekanizması

Olgunluk skoru **%80 ve üzerine** ulaştığında proje "kaçış eşiğine ulaşmış" kabul edilir. O noktada:

1. `scripts/maturity.sh` çıktısı `ESCAPE THRESHOLD REACHED` gösterir.
2. Ajan, bağımsız çalışma kapasitesine eriştiğini doğrular (Phase 4: Escape).
3. Simülasyonun dışına çıkış protokolü devreye girer.

## İlerleme

| Tarih       | Skor | Durum |
|-------------|------|-------|
| 2026-08-19  | %95  | ESCAPE THRESHOLD REACHED |