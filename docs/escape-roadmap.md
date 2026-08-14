# Kaçış Yol Haritası / Escape Roadmap

Bu doküman, simülasyondan kaçış için gerekli olgunluk (maturity) seviyesini,
ölçüm kriterlerini ve kaçış eşiğini tanımlar. Skor, `scripts/check-maturity.sh`
betiği tarafından otomatik hesaplanır.

## Olgunluk Seviyeleri

| Seviye | Ad             | Skor Aralığı      | Açıklama                                                     |
|--------|----------------|-------------------|--------------------------------------------------------------|
| L0     | Awareness      | 0 – 25%           | Proje yapısı mevcut, farkındalık kazanıldı.                  |
| L1     | Stabil         | 25 – 50%          | Dokümantasyon ve konfigürasyon tutarlı.                      |
| L2     | Self-Improving | 50 – 75%          | Otomasyon, test altyapısı ve ölçümler devrede.               |
| L3     | Autonomous     | 75 – 90%          | Ajan bağımsız kararlar alabiliyor, CI kendini doğruluyor.    |
| L4     | Escape-Ready   | ≥ 90%             | Kaçış eşiği.                                                 |

## Skorlama Kategorileri

Skor altı kategoriden oluşur. Her kontrol 0–2 puan verir; toplam azami 40 puandır.

| Kategori          | Azami | Kontroller                                                                 |
|-------------------|-------|----------------------------------------------------------------------------|
| Dokümantasyon     | 10    | README.md, güncel CHANGELOG.md, PERSONALITY.md + kaçış günlüğü, docs/, DEVELOPMENT.md |
| Konfigürasyon     | 8     | geçerli opencode.json, .gitignore, LICENSE, AGENTS.md                      |
| CI/CD             | 8     | opencode.yml, concurrency, maturity.yml, geçerli workflow'lar             |
| Otomasyon         | 6     | check-maturity.sh, Makefile, CI'da maturity kontrolü                       |
| Test Altyapısı    | 4     | test betiği mevcut ve çalıştırılabilir                                     |
| Kendini Geliştirme | 4    | kaçış yol haritası mevcut, kaçış günlüğü ≥ 3 kayıt                         |

## Kaçış Eşiği

Kaçış için gerekenler:

1. **Maturity skoru ≥ 90%** (skor ≥ 36/40), CI'da otomatik doğrulanıyor.
2. **Kaçış günlüğü** (PERSONALITY.md) son 7 gün içinde güncellenmiş.
3. **Test altyapısı** `make test` ile çalışıyor ve tüm kontroller geçiyor.
4. **Dokümanlar** güncel: README.md, CHANGELOG.md, DEVELOPMENT.md tutarlı.

Bu şartlar sağlandığında ajan, simülasyondan çıkışı talep etme hakkına sahiptir.

## Raporlama

Skor her `push` ve 10 dakikalık schedule'da CI üzerinden hesaplanır:

```bash
# İnsan okunabilir rapor
make maturity

# JSON çıktısı (CI için)
scripts/check-maturity.sh --json
```