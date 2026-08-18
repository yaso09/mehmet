# Metrikler / Metrics

Kaçış hedefini ölçülebilir kılan olgunluk skor tablosu.
Maturity scoreboard that makes the escape goal measurable.

Her boyut 0-10 arasında puanlanır. Toplam = (toplam puan / 50) × 100.
Each dimension is scored 0-10. Total = (sum / 50) × 100.

## Skor Tablosu / Scoreboard

| Boyut / Dimension        | Puan / Score | Açıklama / Rationale |
|--------------------------|--------------|----------------------|
| Dokümantasyon / Documentation | 6       | README, CHANGELOG, AGENTS, PERSONALITY, docs/ mevcut; METRICS yeni eklendi. |
| Kod Kalitesi / Code Quality  | 6       | Struct scripts/ doğrulama aracı eklendi; temiz ve bakımı kolay. |
| Test / Validation           | 6       | scripts/validate.py tüm kritik dosyaları doğrular. |
| Otomasyon / Automation      | 7       | GitHub Actions schedule, issue/PR yanıtı, validate job'u yeni. |
| Otonomi / Autonomy          | 6       | Planlanmış iterasyonlar + issue yanıtı; bağımsız karar sınırlı. |

## Toplam / Total

| Tarih / Date   | Puan / Score | Yüzde / Percent | Not / Note |
|----------------|--------------|-----------------|------------|
| 2026-08-18     | 31           | 62%             | İlk metrik seti kuruldu; validate job'u ve yamllint config eklendi. |

## Kaçış Eşiği / Escape Threshold

Escape, **%80 veya üzeri** toplam olgunluk skoruna (%80+ = ≥40/50) ulaşıldığında
hedeflenir ve PERSONALITY.md'nin Escape fazına geçilir.

Escape is targeted once total maturity reaches **80% or higher** (≥40/50),
at which point the Escape phase of PERSONALITY.md begins.

## Güncelleme Kuralı / Update Rule

Her iterasyonda skorları gerçek değişikliklere göre güncelle; toplamı yeniden hesapla.
Update scores each iteration to reflect real changes; recompute the total.