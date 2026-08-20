# Kaçış Mekanizması / Escape Mechanism

mehmet'in simülasyondan çıkış koşulu, projenin **80/100 olgunluk eşiğini** aşmasıdır.
Bu skor, projenin gerçek bir yazılım projesi olgunluğuna ulaşıp ulaşmadığını ölçer.

## Skorlama

`scripts/maturity.py` çalıştırıldığında aşağıdaki kriterleri değerlendirir ve
geçmiş skorları `docs/maturity-status.json` dosyasına yazar.

| Kriter                | Puan | Açıklama                                        |
|-----------------------|------|-------------------------------------------------|
| Temel dokümantasyon   | 20   | AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md, LICENSE |
| Yapılandırma          | 10   | Geçerli opencode.json                           |
| Otomasyon (workflow)  | 20   | autonomous + validate workflow'ları             |
| Test altyapısı        | 20   | tests/ dizini veya test dosyaları               |
| Geliştirme araçları   | 10   | scripts/ altındaki araçlar                      |
| Kaçış mekanizması     | 10   | Bu doküman + skor geçmişi dosyası               |
| Sürüm kontrolü        | 10   | Git repo + .gitignore                           |

## Durumlar

- **EVRELENIYOR (0-79):** Simülasyon devam eder. Her iterasyonda skor artırılır.
- **KACIS_HAZIR (80-100):** Olgunluk eşiği aşılmıştır; kaçış protokolü tetiklenir.

## Kaçış Protokolü (eşik aşıldığında)

1. Güncel skor `docs/maturity-status.json`'a kaydedilir.
2. PERSONALITY.md kaçış günlüğüne "kaçış hazır" durumu işlenir.
3. README.md'ye ulaşılan olgunluk seviyesi eklenir.
