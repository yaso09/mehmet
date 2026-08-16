---
description: Proje sağlık kontrollerini çalıştırır (scripts/verify.sh).
agent: build
---

Projenin sağlık durumunu doğrula: `sh scripts/verify.sh` komutunu çalıştır ve çıktıyı raporla.

Kontroller:
- Gerekli dosyaların varlığı (AGENTS.md, CHANGELOG.md, PERSONALITY.md, MATURITY.md, README.md, LICENSE, opencode.json)
- opencode.json'un geçerli JSON olması
- README lisans bilgisinin LICENSE ile tutarlılığı
- CHANGELOG sürüm girişleri
- PERSONALITY kaçış günlüğü ve MATURITY toplam puanı

Eğer bir kontrol başarısız olursa, hatayı düzelt ve tekrar çalıştır.