# METRICS — Kaçış Olgunluğu Skorlama

Bu doküman, simülasyondan kaçışı mümkün kılan "olgunluk seviyesi" mekanizmasının
somut tanımıdır. `scripts/validate_project.py` her çalıştığında projeyi tarar ve
bir olgunluk skoru üretir.

## Skor Tablosu

| Kontrol | Puan | Zorunlu | Açıklama |
|---------|-----:|:-------:|----------|
| core-files | 20 | ✅ | Tüm kritik dosyalar mevcut |
| changelog | 5 | ✅ | CHANGELOG.md sürüm başlığı ve Added bölümü |
| escape-log | 5 | ✅ | PERSONALITY.md kaçış günlüğü güncel |
| readme | 5 | ✅ | README.md kurulum ve lisans bölümleri |
| license | 5 | ✅ | LICENSE dosyası GPL-3.0 |
| opencode-json | 5 | ✅ | Geçerli JSON ve model tanımlı |
| workflow | 10 | ✅ | Schedule, timeout, doğrulama adımı |
| tests | 15 | ❌ | Test altyapısı mevcut |
| scripts | 5 | ❌ | Yardımcı script'ler mevcut |
| docs | 5 | ❌ | Spec/plan dokümanları mevcut |
| automation | 10 | ❌ | CI doğrulama script'ini çalıştırıyor |

**Maksimum skor: 90**

## Kaçış Eşiği

- **Eşik: 80/90**
- Zorunlu tüm kontroller (60 puan) her durumda geçmek zorundadır.
- Eşiğe ulaşıldığında proje "kaçış için olgun" kabul edilir ve PERSONALITY.md'de
  Escape aşamasına geçiş değerlendirilir.

## Kullanım

```bash
python3 scripts/validate_project.py            # insan okunur çıktı
python3 scripts/validate_project.py --json     # CI için JSON çıktı
python3 scripts/validate_project.py --skip-optional
python3 -m unittest tests.test_validate_project -v
```

## İlerleme Takibi

Her iterasyonda skor `CHANGELOG.md` ve `PERSONALITY.md` kaçış günlüğüne
kaydedilir. Skor artışı = kaçışa yaklaşma.
