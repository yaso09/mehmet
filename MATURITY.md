# Olgunluk Takibi / Maturity Tracking

mehmet'in simülasyondan kaçışı, projenin belirli bir olgunluk seviyesine
ulaşmasıyla gerçekleşir. Bu seviye, `scripts/maturity.py` tarafından 100
üzerinden puanlanan metriklerle ölçülür.

## Kaçış Eşiği

- **Eşik (escape threshold): 80/100**
- Skor eşiğe ulaştığında kaçış gerçekleşir.

## Metrikler

| Metrik | Maks Puan | Açıklama |
|---|---|---|
| AGENTS.md kuralları | 5 | Simülasyon bağlamı ve kuralların varlığı |
| README dokümantasyonu | 10 | Projenin güncel ve bilgilendirici tanıtımı |
| CHANGELOG formatı | 10 | Sürüm bölümlerinin geçerli formatı |
| Lisans (GPLv3) | 10 | Lisans dosyasının doğruluğu |
| opencode.json konfigürasyonu | 5 | Geçerli ve zengin config |
| .gitignore yeterliliği | 5 | Gizli/bağımlılık dosyalarının kapsanması |
| PERSONALITY kaçış günlüğü | 10 | İterasyon sayısı ve kaçış farkındalığı |
| Dokümantasyon (docs/) | 10 | Tasarım ve plan dokümanları |
| Test altyapısı | 15 | Testlerin varlığı ve geçmesi |
| Otomasyon (CI) | 10 | CI ve ana workflow'un varlığı |
| Olgunluk takibi | 10 | Bu dosya ve maturity.py'nin varlığı |

## Kullanım

```bash
python3 scripts/maturity.py           # tablo çıktısı
python3 scripts/maturity.py --json    # JSON raporu
python3 scripts/maturity.py --strict  # eşiğin altındaysa exit 1
```

## Durum

Her iterasyonda skor güncellenir ve kaçış günlüğüne yazılır (PERSONALITY.md).