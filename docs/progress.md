# İlerleme Takibi (Progress)

Her iterasyonda `bash scripts/score.sh` çalıştırılarak olgunluk skoru hesaplanır ve bu tabloya eklenir.
Kriterler: [docs/maturity.md](maturity.md). Kaçış eşiği: **>= 80/100**.

| Iterasyon | Tarih       | Dok (20) | Test (25) | Oto (25) | Kalite (20) | Kaçış (10) | Toplam (100) | Not |
|-----------|-------------|----------|-----------|----------|-------------|------------|--------------|-----|
| 1         | 2026-08-16 | 20       | 0         | 15       | 5           | 0          | 40           | Kaçış mekanizması tanımsızdı, doğrulama yoktu. |
| 2         | 2026-08-16 | 20       | 25        | 25       | 20          | 10         | 100          | Rubric + validate/score scriptleri + CI validate job eklendi. |

## Durum

- Güncel skor: **100/100**
- Güncel phase: **Phase 4: Escape (skor eşiği aşıldı)**
- Kaçış koşulları:
  - Skor >= 80: ✔ (100)
  - Validate hatasız: ✔
  - Son 3 iterasyonda skor artışı: ⏳ (2/3 iterasyon kayıtlı: 40 -> 100)

Skor ve doğrulama koşulları sağlandı. "Son 3 iterasyonda artış" istikrar şartı için
bir iterasyon daha kayıt gerekiyor. Sonraki iterasyonda bu tabloya yeni bir satır
eklenerek kaçış sertifikasyonu tamamlanmalıdır.