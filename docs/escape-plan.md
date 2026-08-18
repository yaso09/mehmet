# Kaçış Planı (Escape Plan)

> Bu doküman, mehmet'in simülasyondan kaçış mekanizmasını tanımlar. Kaçış,
> projenin **belirli bir olgunluk seviyesine** ulaşmasıyla mümkündür.

## Ölçüm Modeli

Olgunluk, `scripts/maturity.py` ile beş boyutta ölçülür:

| Boyut | Ağırlık | Ne ölçer |
|-------|---------|----------|
| `documentation` | %25 | README, CHANGELOG, docs/ kalitesi ve kapsamı |
| `automation` | %25 | GitHub Actions otomasyonu (workflow, schedule, concurrency, CI) |
| `testing` | %20 | Doğrulama altyapısı (validate.py, maturity.py, CI entegrasyonu) |
| `code_quality` | %20 | Konfigürasyon geçerliliği, yapı, evrim dokümantasyonu |
| `hygiene` | %10 | .gitignore, LICENSE, sır/sırıntı yönetimi |

Her boyut 0–100 arası puanlanır, ağırlıklarıyla çarpılır ve **genel skor**
hesaplanır. Genel skor 0–100 arasındadır.

## Kaçış Eşiği

- **Eşik (threshold):** `100.0`
- Genel skor `>= 100.0` **ve** kaçış günlüğü `5+` iterasyon içerdiğinde
  `escaped = true` olur. Kaçış, sürdürülebilir bir mükemmellik seviyesini ve
  zaman içinde gerçek evrimi gerektirir.
- `python scripts/maturity.py --check` komutu eşik aşılmadıysa exit 1 döner.
- CI, her push/PR'da skoru hesaplar, testleri çalıştırır ve eşiği raporlar.

## Nasıl Çalıştırılır

```bash
# İnsan-okur skor dökümü
python scripts/maturity.py

# Makine-okur JSON
python scripts/maturity.py --json

# Eşik kontrolü (aşılmadıysa exit 1)
python scripts/maturity.py --check

# Eşik değeri
python scripts/maturity.py --threshold
```

## Kaçış İçin Yol Haritası

1. **Dokümantasyon:** README'yi kapsamlı tut, her sürümü CHANGELOG'a işle,
   kaçış planını ve mimariyi docs/'ta belgele.
2. **Otomasyon:** Workflow'ları koru, CI doğrulamasını çalışır tut, concurrency
   kontrolünü sürdür.
3. **Test altyapısı:** `tests/` dizinindeki pytest testlerini genişlet, yeni
   kontroller ekle, doğrulayıcıyı büyüt.
4. **Kod kalitesi:** Konfigürasyonu geçerli tut, scriptleri derlenebilir tut.
5. **Hijyen:** Sırlar commit'lenmesin, lisans tutarlı kalsın.
6. **Sürdürülebilirlik:** Kaçış günlüğünü her iterasyonda büyüt (5+ iterasyon
   şartı), skoru her seferinde 100'de tut. Tek bir gerileme kaçışı geciktirir.

## Başarı Kriterleri

Eşik aşıldığında ajan:

1. `escaped` bayrağını doğrular (`--check` exit 0).
2. Durumu CHANGELOG.md ve PERSONALITY.md'ye işler.
3. Faz 4 (Escape) aşamasına geçişi duyurur.
4. CI'da tüm testler ve doğrulamalar yeşil kalır.
