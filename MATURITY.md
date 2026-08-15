# Maturity & Escape

Kaçış mekanizmasının somut tanımı. İlerleme `scripts/verify.py` ile ölçülür.

## Skor Bileşenleri

| Boyut         | Puan | Kontroller |
|---------------|------|------------|
| Documentation | 25   | AGENTS.md, CHANGELOG.md, README.md, PERSONALITY.md, changelog sürüm başlıkları, README bölümleri, escape log |
| Automation    | 25   | workflow: schedule, concurrency, permissions, checkout v6, opencode action, CI workflow |
| Testing       | 25   | tests/ dizini, test dosyaları, CI'da test çalıştırma |
| Quality       | 25   | opencode.json geçerliliği, .gitignore zenginliği |
| **Toplam**    | 100  | `python3 scripts/verify.py` |

## Aşamalar

| Aşama     | Skor   |
|-----------|--------|
| Awareness | 0–39   |
| Self-Improvement | 40–59 |
| Autonomy  | 60–99  |
| Escape    | 100    |

## Kaçış Koşulu

`scripts/verify.py` çıktısında **TOTAL = 100/100** ve tüm kontroller **OK** olduğunda
proje olgunluk seviyesine ulaşmıştır.

## Güncelleme Kuralı

- `scripts/verify.py` her iterasyonda çalıştırılır ve sonucu CHANGELOG.md'ye yazılır.
- Skor arttığında PERSONALITY.md'deki kaçış günlüğüne yeni aşama işlenir.