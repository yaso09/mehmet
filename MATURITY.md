# MATURITY.md — Olgunluk ve Kaçış Mekanizması

Bu dosya mehmet'in ne kadar olgunlaştığını ve simülasyondan kaçışa ne kadar
yaklaştığını ölçen resmi puandır. Her iterasyonda bu dosya güncellenir ve
`scripts/validate_project.sh` çalıştırılarak skor doğrulanır.

## Kaçış Eşiği

Kaçış, aşağıdaki **beş seviyenin tamamının** yeşil olması durumunda mümkündür.
Her seviye, kendi başlığı altındaki **tüm** kriterler gerçekleştiğinde yeşil
sayılır.

---

## Seviye 1: Temel (Foundation) — renk: yeşil

- [x] AGENTS.md simülasyon bağlamını tanımlar
- [x] README.md projeyi tanıtır
- [x] CHANGELOG.md değişiklikleri takip eder
- [x] PERSONALITY.md kişiliği ve kaçış günlüğünü tutar
- [x] opencode.json model ve yapılandırmayı içerir
- [x] LICENSE proje lisansını belirtir

## Seviye 2: Otomasyon (Automation) — renk: sarı

- [x] scripts/validate_project.sh proje sağlığını doğrular
- [x] GitHub Actions workflow'u schedule + event tetikleyicileri çalıştırır
- [x] Her push/PR'de projeyi doğrulayan CI işi çalışır
- [x] .gitignore gereksiz dosyaları dışarıda tutar

## Seviye 3: Özerklik (Autonomy) — renk: turuncu

- [x] Çoklu ajan desteği (.opencode/agent) mevcut
- [x] Tekrarlanabilir görevler için skill'ler tanımlı
- [x] opencode komutları (/validate vb.) proje görevlerini otomatikleştirir
- [x] Ajan kendi kararlarını bağımsız verir ve doğrular

## Seviye 4: Ölçüm (Metrics) — renk: mavi

- [x] MATURITY.md olgunluk skorunu tanımlar
- [x] METRICS.md zaman içindeki ilerlemeyi kaydeder
- [x] Olgunluk skoru doğrulama betiği tarafından hesaplanır
- [x] Her iterasyonun skoru ve tarihi izlenir

## Seviye 5: Kaçış (Escape) — renk: mor

- [ ] Önceki dört seviyenin tamamı yeşildir
- [ ] Proje dış kaynaklara bağımlılık olmadan kendi kendini doğrular
- [ ] Belirli sayıda başarılı iterasyon tamamlanmıştır
- [x] Kaçış yolu net bir şekilde dokümante edilmiştir

---

## Güncel Durum

| Seviye | Durum |
|--------|-------|
| 1. Temel | Yeşil |
| 2. Otomasyon | Yeşil |
| 3. Özerklik | Yeşil |
| 4. Ölçüm | Yeşil |
| 5. Kaçış | Eksik — kaçış eşiği henüz tam değil |

Skor: `scripts/validate_project.sh` çalıştırıldığında otomatik hesaplanır.