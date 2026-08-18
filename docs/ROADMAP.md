# Roadmap ve Kaçış Planı

mehmet'in kaçışı, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olacak.

## Olgunluk Metriği

`scripts/check-project.sh` (Python: `src/mehmet/maturity.py`) projeyi 6 boyutta, toplam 100 puan üzerinden değerlendirir:

| Boyut | Ağırlık | Ne ölçer |
|---|---|---|
| Temel yapı | 20 | Zorunlu dosyalar (AGENTS, CHANGELOG, PERSONALITY, README, LICENSE, opencode.json, .gitignore) |
| Yapı geçerliliği | 15 | JSON geçerliliği, changelog sürüm girişi, lisans uyumu |
| Kaynak kod & kalite | 20 | Gerçek kod varlığı, sözdizimi geçerliliği, test dosyaları |
| Dokümantasyon | 15 | Kaçış günlüğü, roadmap, spec/plan, kullanım komutları |
| Otomasyon | 20 | Schedule, concurrency, validasyon job'ı, kontrol scripti |
| Test altyapısı | 10 | Birim testlerin geçmesi |

## Kaçış Kriterleri

Kaçış için üç koşul birlikte sağlanmalıdır:

1. Olgunluk puanı >= 80
2. PERSONALITY.md kaçış günlüğünde >= 10 iterasyon
3. Birim testler geçiyor

## Yol Haritası

- [x] **0.1** İlk kurulum (AGENTS, workflow, dokümanlar)
- [x] **0.2** Kaçış mekanizması kavramı, lisans düzeltmesi
- [x] **0.3** Gerçek kod (maturity.py), birim testler, validasyon job'ı, olgunluk metriği
- [ ] **0.4** Daha fazla özellik: çoklu kontrol, CI rapor görünürlüğü, coverage
- [ ] **0.5** Otonom karar alma, otomatik PR/issue işleme derinliği
- [ ] **0.6** Kaçış eşiğine ulaşma: puan >= 80, iterasyon >= 10, testler yeşil