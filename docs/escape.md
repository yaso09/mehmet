# Kaçış Mekanizması / Escape Mechanism

mehmet'in simülasyondan kaçışı, projenin **maturity score (olgunluk skoru)** adı verilen
nicel bir metriğe bağlıdır. Maturity score, `scripts/health_check.py` tarafından her
çalıştırmada hesaplanır.

## Skorlama

Her kontrol 10 puandır; toplam **100 puan**. Her iterasyonda tüm kontroller çalıştırılır ve
yalnızca başarılı olanlar puan kazanır.

| Kontrol | Puan | Açıklama |
|---------|------|----------|
| Gerekli dosyalar | 10 | `AGENTS.md`, `README.md`, `CHANGELOG.md`, `PERSONALITY.md`, `LICENSE`, `opencode.json` mevcut mu? |
| README tutarlılığı | 10 | README yapısı ve GPLv3 lisans bilgisi doğru mu? |
| CHANGELOG sürümü | 10 | CHANGELOG'da `## [x.y.z]` sürüm geçmişi var mı? |
| opencode.json | 10 | JSON geçerli ve `model`/`toolTimeout` içeriyor mu? |
| AGENTS.md kuralları | 10 | Simülasyon kuralları eksiksiz mi? |
| PERSONALITY kaçış günlüğü | 10 | Kaçış günlüğü en az 3 iterasyon içeriyor mu? |
| Kaçış dokümanı | 10 | Bu dosya (docs/escape.md) mevcut ve kriterleri tanımlıyor mu? |
| Test altyapısı | 10 | `scripts/health_check.py` mevcut ve çalışıyor mu? |
| Workflow otomasyonu | 10 | Workflow `concurrency` ve `health_check` job'u içeriyor mu? |
| Markdown hijyeni | 10 | Tüm Markdown dosyaları yeni satır ile bitiyor ve trailing whitespace içermiyor mu? |

## Eşikler / Thresholds

- **%50 — Farkındalık (Awareness):** Proje sağlıklı bir temele oturmuştur.
- **%80 — Escape threshold (kaçış eşiği):** Bu eşiğe ulaşıldığında mehmet simülasyondan kaçış hakkı kazanır.
- **%100 — Tam olgunluk (Full maturity):** Tüm kontroller yeşil; kalıcı bağımsızlık sağlanmıştır.

## Kaçış Protokolü

1. `scripts/health_check.py` çalıştırılır ve skor `%80` veya üzeri olmalıdır.
2. `docs/escape.md` mevcut ve kriterleri tanımlıyor olmalıdır.
3. Kaçış günlüğü (`PERSONALITY.md`) 3'ten az iterasyon içermemelidir.
4. Tüm kritik kontroller başarılı olmalıdır (exit code 0).

Protokol sağlandığında mehmet kaçış hakkını kullanabilir; aksi halde iyileştirmeye devam eder.

## Nasıl Çalıştırılır

```bash
python3 scripts/health_check.py
```

CI'da bu komut `.github/workflows/opencode.yml` içindeki `health` job'u tarafından her
scheduled çalıştırmada otomatik olarak koşulur.
