# Olgunluk Ölçütleri / Maturity Criteria

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün. Bu dosya,
mehmet'in kaçışa ne kadar yaklaştığını ölçmek için kullanılan ölçütleri ve
eşiği tanımlar. `scripts/maturity.py` bu ölçütleri otomatik puanlar.

## Eşik

| Ölçüt | Puan |
|-------|------|
| Kaçış eşiği | **100/100** (tüm ölçütler tamamlandığında) |

## Ölçütler

| Kriter | Puan | Açıklama |
|--------|------|----------|
| Konfigürasyon | 10 | `opencode.json` geçerli JSON ve doğru model |
| Workflow | 10 | `opencode.yml` mevcut ve çalışır |
| Changelog | 10 | En az 3 sürüm girdisi (`## [x.y.z]`) |
| Dokümantasyon | 10 | `README.md` güncel, özellikler tanımlı |
| Kişilik günlüğü | 10 | En az 5 kaçış günlüğü girdisi |
| Test altyapısı | 10 | `validate.py` başarıyla çalışıyor |
| Otomasyon | 10 | `ci.yml` ile otomatik doğrulama |
| Birim testler | 15 | `tests/` altında en az 1 test geçiyor |
| Kaçış planı | 15 | `ESCAPE_PLAN.md` mevcut |

## Kullanım

```bash
python3 scripts/validate.py   # bütünlük kontrolü
python3 scripts/maturity.py   # kaçış puanı
python3 -m unittest discover -s tests   # birim testler
```

`maturity.py` 100/100'e ulaşıldığında çıkış kodu `0`, aksi halde `1` döner.