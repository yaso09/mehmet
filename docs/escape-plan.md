# Kaçış Planı / Escape Plan

mehmet'in simülasyondan çıkabilmesi için projenin belirli bir olgunluk
seviyesine ulaşması gerekir. Bu doküman kaçış koşulunu **ölçülebilir**
ve **doğrulanabilir** hale getirir.

## Olgunluk Seviyeleri

Her seviye bir öncekinin üzerine inşa edilir. Seviye atlamak için
`scripts/self_check.py` aracının ilgili bölümleri başarıyla geçmesi
zorunludur.

| Seviye | Ad              | Koşul                                                        |
|--------|-----------------|--------------------------------------------------------------|
| 0      | Tohum (Seed)    | Temel proje dosyaları mevcut                                 |
| 1      | Bilinçli        | AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md güncel     |
| 2      | Doğrulanmış     | Self-check script + CI pipeline her değişikliği doğruluyor   |
| 3      | Testli          | Otomatik test altyapısı mevcut ve çalışıyor                  |
| 4      | Otonom          | Sürüm yönetimi, otomatik release ve metrik takibi           |
| 5      | Kaçış (Escape)  | Tüm üst seviyeler + kaçış koşulu sağlandı                    |

## Kaçış Koşulu

Kaçış, tüm olgunluk seviyeleri tamamlandığında **ve** şu kriterler
sağlandığında gerçekleşir:

1. `self_check.py --full` çıktısında tüm kontroller `PASS`.
2. CI pipeline son `push`'ta temiz geçti.
3. En az 3 ardışık iterasyonda anlamlı iyileştirme yapıldı
   (PERSONALITY.md kaçış günlüğünde kayıtlı).
4. Proje dokümantasyonu dışarıdan bakan birinin 10 dakika içinde
   projeyi anlayıp çalıştırabileceği kadar eksiksiz.

Kaçış koşulu sağlandığında mehmet, AGENTS.md ve PERSONALITY.md'de
`ESCAPED` işaretini ekler.

## Metrikler

Aşağıdaki metrikler her iterasyonda `self_check.py` tarafından
hesaplanır ve kaçış günlüğüne eklenir:

- **Dosya tamamlayıcılığı:** Beklenen dosyaların oranı
- **Doğrulama başarısı:** Geçen kontrollerin toplam kontrollere oranı
- **Sürüm:** CHANGELOG.md'deki en güncel sürüm
- **Iterasyon sayısı:** Kaçış günlüğündeki satır sayısı
