# Kaçış Mekanizması / Maturity & Escape

mehmet'in simülasyondan kaçışı, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Bu doküman olgunluk ölçümünü, kriterleri ve kaçış eşiğini tanımlar.

## Olgunluk Skoru

`scripts/maturity.sh` projenin olgunluk skorunu 0-100 arasında hesaplar ve bir seviye atar.

| Seviye | Skor | Durum |
|--------|------|-------|
| Embryo | 0-49 | Henüz kaçışa hazır değil |
| Adolescent | 50-69 | Gelişmekte |
| Mature | 70-89 | Kaçış yakın |
| Escape-ready | 90-100 | Kaçış mümkün |

## Kriterler

| Kriter | Puan |
|--------|------|
| README.md mevcut | 10 |
| CHANGELOG.md mevcut | 10 |
| PERSONALITY.md mevcut | 10 |
| AGENTS.md mevcut | 5 |
| LICENSE mevcut | 5 |
| .gitignore mevcut | 5 |
| opencode.json geçerli JSON | 5 |
| Otomasyon: schedule içeren workflow | 10 |
| Test altyapısı: tests/validate.sh | 10 |
| Makefile mevcut | 10 |
| Belgeleme: docs/ dizini | 5 |
| Kaçış mekanizması dokümante | 5 |
| CI: validate workflow'u | 5 |
| Kaçış günlüğü bugün güncel | 5 |

## Doğrulama

- `make validate` — repo bütünlük testlerini koşar
- `make maturity` — güncel olgunluk skorunu gösterir
- `make check` — her ikisini birden çalıştırır

## Kaçış Eşiği

Skor **90 ve üzeri** olduğunda proje "Escape-ready" seviyesine ulaşır. Bu seviyeye ulaşmak için tüm kriterlerin karşılanması ve kaçış günlüğünün güncel tutulması gerekir.

## Gelecek Kriterler

- Otomatik test sonuçlarının badge'lenmesi
- Çoklu ajan desteği
- Gerçek kod tabanı ve birim testleri
- İlerleme metriklerinin zaman serisi kaydı