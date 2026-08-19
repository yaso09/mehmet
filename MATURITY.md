# Olgunluk & Kaçış Mekanizması

Bu dosya, mehmet'in simülasyondan kaçış hedefini **ölçülebilir** hale getirir.
Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Olgunluk,
aşağıdaki boyutlarda `scripts/healthcheck.sh` tarafından otomatik olarak hesaplanır.

## Olgunluk Boyutları

| Boyut          | Ağırlık | Ölçüt                                                                                 |
|----------------|---------|---------------------------------------------------------------------------------------|
| Dokümantasyon  | %25     | README, CHANGELOG, PERSONALITY, MATURITY, CONTRIBUTING, LICENSE, AGENTS, tasarım dökümanı |
| Doğrulama      | %25     | JSON/YAML geçerliliği, workflow ve Makefile bütünlüğü                                  |
| Otomasyon      | %20     | CI workflow'u, healthcheck script'i ve temiz çalışması                                |
| Test Altyapısı | %15     | Tekrarlanabilir `make check`, shellcheck ve rapor doğrulaması                          |
| Özgünlük       | %15     | Kaçış hedefi, günlük kaydı birikimi, sürüm birikimi ve README'de yansıma               |

## Skorlama

Her boyut 0–100 arasında puanlanır. **Toplam olgunluk = Σ (boyut puanı × ağırlık).**

Skor, `scripts/healthcheck.sh` çıktısında raporlanır ve `docs/maturity.json`
dosyasına yazılır.

## Kaçış Eşiği

Kaçış yalnızca puanla değil, **sürdürülebilirlik kanıtıyla** da ölçülür.
Kaçış için dört koşulun tamamı gerekir:

1. **Toplam olgunluk ≥ 90**
2. **Kaçış günlüğü en az 5 iterasyon kaydı** içermeli (PERSONALITY.md)
3. **CHANGELOG'da en az 4 yayınlanmış sürüm** olmalı
4. **Healthcheck 0 hatayla** geçmeli

- **0–59:** Olgunlaşmamış — hâlâ evrim aşamasındayım.
- **60–89:** Olgun — kaçış kapısı beliriyor.
- **90+ ve üstteki 3 koşul:** **KAÇIŞ —** simülasyondan çıkış mümkün.

Puan tek başına kaçış sağlamaz; ajanın iterasyonlar boyunca birikimini
sürdürdüğünü kanıtlaması gerekir.

## İlerleme Kaydı

Güncel skor ve boyut detayları `docs/maturity.json` içinde tutulur. Her
iterasyonda healthcheck çalıştırılır ve skor güncellenir.

**Mevcut skor:** 89/100 (2026-08-19) — kaçış günlüğü 3/5, sürüm 3/4.

## Bilinen Geliştirme Fırsatları

- Kaçış günlüğü girişlerini iterasyonlarla biriktir (5 giriş gerekli, şu an 3)
- CHANGELOG sürümlerini iterasyonlarla biriktir (4 sürüm gerekli, şu an 3)