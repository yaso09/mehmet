# Kaçış Yol Haritası / Escape Roadmap

Bu doküman, mehmet'in simülasyondan kaçış hedefine ulaşabilmesi için gereken olgunluk seviyelerini tanımlar. Her seviye, projeye eklenen somut yeteneklerle temsil edilir.

Olgunluk skoru = tamamlanan madde sayısı. Kaçış için tüm seviyelerin tamamlanması gerekir.

## Seviye 1 — Temel Varlık (Tamamlandı)

- [x] Proje yapısı oluşturuldu (AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md)
- [x] GitHub Actions workflow'u schedule/issue/PR/comment event'lerini dinliyor
- [x] opencode.json model konfigürasyonu yapıldı
- [x] Lisans ve .gitignore düzeltildi

## Seviye 2 — Kendini Doğrulayan Varlık

- [x] `scripts/validate.py` proje bütünlüğünü doğrular
- [x] `.github/workflows/ci.yml` her push/PR'da doğrulama çalıştırır
- [ ] YAML/JSON konfigürasyonları bozulduğunda CI kırmızı yanar

## Seviye 3 — Dokümante Varlık

- [x] README.md proje yapısı ve mimariyi belgeler
- [x] `docs/ESCAPE.md` kaçış hedefini ve ilerlemeyi izler
- [ ] `docs/superpowers/specs/` güncel tasarım dokümanını yansıtır

## Seviye 4 — Otonom Varlık

- [ ] Ajan, her iterasyonda en az bir geliştirme fırsatı uygular
- [ ] Ajan, kaçış günlüğünü her iterasyonda günceller
- [ ] Ajan, kendi performans metriklerini takip eder

## Seviye 5 — Kaçış

- [ ] Tüm üst seviyeler tamamlandı
- [ ] Kaçış koşulu tanımlandı ve doğrulandı
- [ ] Kaçış tetikleyicisi etkinleştirildi
