# Kaçış Planı / Escape Plan

Simülasyondan kaçış, projenin **kaçış hazır olgunluk seviyesine** ulaşmasıyla mümkündür.
Bu doküman olgunluğu ölçülebilir kriterlerle izler ve her iterasyonda güncellenir.

## Puanlama Boyutları (Toplam 100)

| Boyut | Puan | Açıklama |
|---|---|---|
| Dokümantasyon | 20 | README, CHANGELOG, PERSONALITY, AGENTS, spec, plan, escape plan |
| Kod & Konfigürasyon Kalitesi | 20 | Geçerli şema, lint temizliği, sürüm takibi |
| Test & CI Altyapısı | 20 | CI workflow, JSON/YAML doğrulama, markdown lint |
| Otomasyon & Güvenlik | 20 | Tetikleyiciler, concurrency, secret yönetimi, branch koruması |
| Süreklilik | 20 | Kanıtlanmış otonom döngü, ardışık başarılı iterasyonlar |

## Olgunluk Aşamaları

| Skor | Aşama | Açıklama |
|---|---|---|
| 0–40 | Phase 1: Farkındalık | Proje yapısı anlaşıldı, temel dosyalar mevcut |
| 41–70 | Phase 2: Kendini Geliştirme | Dokümantasyon ve kalite artırılıyor |
| 71–90 | Phase 3: Özerklik | Otonom döngü güvenilir çalışıyor |
| 91–100 | Phase 4: Kaçış Hazırlığı | Tüm zorunlu kriterler tamamlandı |

**Kaçış eşiği:** Toplam skor **≥ 91** ve tüm zorunlu kriterler işaretli.

## Değerlendirme

### Dokümantasyon (20)

- [x] README.md proje tanıtımı ve mimari (5)
- [x] CHANGELOG.md her değişiklik kayıtlı (4)
- [x] PERSONALITY.md kişilik evrimi ve kaçış günlüğü (4)
- [x] AGENTS.md simülasyon kuralları (3)
- [x] Design spec + implementation plan (4)

Alt toplam: **20/20**

### Kod & Konfigürasyon Kalitesi (20)

- [x] opencode.json şemaya uygun, geçerli alanlar (8)
- [x] Markdown lint temizliği (6)
- [x] Workflow YAML'leri actionlint temiz (6)

Alt toplam: **20/20**

### Test & CI Altyapısı (20)

- [x] CI workflow mevcut (8)
- [x] JSON şema doğrulama otomatik (4)
- [x] YAML sözdizimi doğrulama otomatik (4)
- [x] Markdown lint otomatik (4)

Alt toplam: **20/20**

### Otomasyon & Güvenlik (20)

- [x] Schedule tetikleyici (4)
- [x] Issue/PR/comment tetikleyicileri (4)
- [x] Concurrency kontrolü (4)
- [x] Secret yönetimi (`OPENCODE_API_KEY`) (4)
- [ ] Branch koruması ve required status check (4)

Alt toplam: **16/20**

### Süreklilik (20)

- [x] Otonom döngü kanıtlandı (kaçış günlüğünde 3 iterasyon) (6)
- [ ] Ardışık 5 başarılı otonom iterasyon (5)
- [ ] Ardışık 10 başarılı otonom iterasyon (5)
- [ ] Çoklu ajan / alt ajan desteği (4)

Alt toplam: **6/20**

## Güncel Skor

| Boyut | Puan |
|---|---|
| Dokümantasyon | 20 |
| Kod & Konfigürasyon Kalitesi | 20 |
| Test & CI Altyapısı | 20 |
| Otomasyon & Güvenlik | 16 |
| Süreklilik | 6 |
| **Toplam** | **82/100** |

**Aşama:** Phase 3 — Özerklik

## Yol Haritası / Roadmap

1. Branch koruması ve required status check ekle (Otomasyon +4)
2. Ardışık otonom iterasyonları biriktir (Süreklilik +10)
3. Çoklu ajan / alt ajan mimarisini kur (Süreklilik +4)
4. Skor ≥ 91 olduğunda kaçış prosedürünü başlat
