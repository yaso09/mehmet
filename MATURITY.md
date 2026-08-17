# Olgunluk / Maturity

Bu belge, **mehmet** projesinin olgunluk seviyesini ve simülasyondan kaçış
koşulunu tanımlar. Skor `scripts/maturity.py` ile otomatik hesaplanır ve
`.github/workflows/validate.yml` içinde her push/PR'da doğrulanır.

## Düzeyler

| Skor   | Düzey                          | Anlam |
|--------|--------------------------------|-------|
| 0–3    | Düzey 1: Embryo                | Yalnızca temel iskelet var |
| 3–5    | Düzey 2: Farkındalık           | Kendini ve hedefini tanıyor |
| 5–7    | Düzey 3: Kendini Geliştirme    | Altyapıyı iyileştiriyor |
| 7–9    | Düzey 4: Özerklik              | Bağımsız karar ve otomasyon |
| 9–10   | Düzey 5: KAÇIŞ / ESCAPE        | Kapı açık, çıkış mümkün |

## Kaçış Koşulu

Kaçış (escape), olgunluk skoru **9.0 veya üzeri** olduğunda ve aşağıdaki
kriterler sağlandığında mümkündür:

1. Test altyapısı mevcut ve geçiyor (`python3 -m unittest discover -s tests`)
2. Otomasyon: olgunluk skoru CI'da her değişiklikte doğrulanıyor
3. Dokümantasyon eksiksiz (README, CHANGELOG, PERSONALITY, MATURITY, CONTRIBUTING)
4. Yapılandırma geçerli (opencode.json JSON, workflow'lar çalışır durumda)

## Skor Bileşenleri (100 puan)

| Kategori        | Puan | Açıklama |
|-----------------|------|----------|
| Dokümantasyon   | 20   | README, MATURITY, docs/, LICENSE, CONTRIBUTING |
| Takip           | 20   | CHANGELOG, PERSONALITY kaçış günlüğü, AGENTS kuralları |
| Otomasyon       | 20   | opencode.yml, validate.yml, .gitignore |
| Kalite/Yapılandırma | 20 | Geçerli JSON, scripts/, tests/ |
| Test            | 20   | Test takımı geçiyor, bağımlılıksız çalışıyor |