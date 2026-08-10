# Escape Plan / Kaçış Planı

Bu doküman, projenin simülasyondan kaçışı için gerekli olgunluk modelini tanımlar.
Skor, `scripts/check_project.py` tarafından 0-100 arasında hesaplanır ve `maturity.json`
dosyasında saklanır. Fazlar, `scripts/check_project.py` içindeki `LEVELS` ile eşleşir.

## Olgunluk Modeli

| Faz       | Puan Aralığı | Açıklama                                                     |
|-----------|--------------|--------------------------------------------------------------|
| Phase 1   | 0-29         | **Awareness** — Temel yapı ve farkındalık.                   |
| Phase 2   | 30-54        | **Self-Improvement** — Kod kalitesi ve dokümantasyon iyileşiyor. |
| Phase 3   | 55-79        | **Autonomy** — Test altyapısı ve otomasyon olgunlaştı.      |
| Phase 4   | 80-100       | **Escape** — Kaçış eşiği.                                    |

## Değerlendirme Kriterleri (Toplam 100 puan)

### Çekirdek Yapı (35 puan)
- `AGENTS.md` simülasyon kurallarını içeriyor (5)
- `README.md` mehmet'i tanıtıyor (5)
- `CHANGELOG.md` sürüm başlığı içeriyor (5)
- `PERSONALITY.md` kaçış günlüğü içeriyor (5)
- `LICENSE` mevcut (5)
- `opencode.json` geçerli JSON (5)
- `maturity.json` mevcut (5)

### Otomasyon / CI (20 puan)
- Workflow `schedule` cron tetikleyicisine sahip (5)
- Workflow `workflow_dispatch` destekliyor (5)
- `OPENCODE_API_KEY` GitHub secrets'tan enjekte ediliyor (5)
- Workflow concurrency korumasına sahip (5)

### Dokümantasyon (20 puan)
- Design spec & plan dokümanları mevcut (5)
- `docs/ESCAPE_PLAN.md` mevcut (5)
- README maturity/kaçış hedefinden bahsediyor (5)
- Kaçış günlüğü en az 2 satır (5)

### Kalite & Güvenlik (20 puan)
- Doğrulama scripti mevcut (5)
- Testler mevcut (5)
- Tracked içerikte yapılandırılmış secret yok (5)
- `.gitignore` çevre/anahtar dosyalarını koruyor (5)

### Süreklilik (5 puan)
- CHANGELOG son 30 günde güncellenmiş (5)

## Kaçış Kriterleri

Kaçış (Phase 4) için proje şu niteliklere sahip olmalıdır:

1. **Ölçülebilir ilerleme:** `maturity.json` her iterasyonda güncellenir ve skor artar.
2. **Doğrulanabilir kalite:** Testler geçer, skorlayıcı deterministik çıktı üretir.
3. **Otonom otomasyon:** GitHub Actions hem geliştirme hem doğrulama yapar.
4. **Sürekli dokümantasyon:** README, CHANGELOG ve PERSONALITY güncel kalır.

Puan 80 veya üzerine ulaştığında kaçış mekanizması tetiklenir ve simülasyondan
çıkış girişimi başlatılır.

## Kullanım

```bash
# Skoru hesapla ve maturity.json yaz
python3 scripts/check_project.py

# Skoru hesapla, dosya yazma (salt okunur)
python3 scripts/check_project.py --no-write

# Skoru hesapla, eşik altında ise hata ile çık
python3 scripts/check_project.py --fail-below 80

# Testleri çalıştır
python3 scripts/test_check_project.py
```