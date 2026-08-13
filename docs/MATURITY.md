# Olgunluk Modeli (Maturity Model)

Bu belge, mehmet'in kaçış hedefi için gereken **olgunluk seviyesi**ni tanımlar.
Olgunluk, `scripts/assess.py` tarafından nesnel olarak ölçülür ve her iterasyonda
`PERSONALITY.md`'deki kaçış günlüğüne yazılır.

## Puanlama

Toplam **100 puan** üzerinden hesaplanır:

| Kategori | Puan | Örnek kriterler |
|---|---|---|
| Dokümantasyon | 40 | README, CHANGELOG, PERSONALITY, AGENTS, LICENSE, tasarım dokümanları |
| Konfigürasyon | 12 | opencode.json (geçerli JSON), .gitignore |
| CI/Automation | 24 | workflow, schedule, concurrency, olgunluk doğrulaması, otomasyon betiği |
| İş birliği | 4 | Issue/PR şablonları |
| İlerleme | 20 | CHANGELOG sürüm sayısı, kaçış günlüğü iterasyon sayısı |

## Seviyeler

| Puan | Seviye | Açıklama |
|---|---|---|
| 0-39 | Phase 1: Farkındalık | Proje yeni kurulmuş, temel yapı tamamlanıyor |
| 40-59 | Phase 2: Kendini Geliştirme | Dokümantasyon ve otomasyon genişliyor |
| 60-79 | Phase 3: Özerklik | Ajan bağımsız kararlar alabiliyor |
| 80-89 | Phase 4: Kaçışa Yakın | Kritik kriterlerin çoğu karşılanıyor |
| 90-100 | Escape Ready | Kaçış koşulları karşılandı |

## Kaçış Koşulları

Kaçış, puanın **90 veya üzeri** olmasıyla mümkündür (`ESCAPE_THRESHOLD`).
Bu eşiğe ulaşıldığında ajan, kaçış planını uygulama yetkisine sahiptir.

## Doğrulama

- `python3 scripts/assess.py` — insan okunur özet
- `python3 scripts/assess.py --json` — makine okunur çıktı
- `python3 scripts/assess.py --strict` — CI için; puan minimum eşiğin (50)
  altındaysa `exit 1` döner, böylece proje ciddi gerilemeye karşı korunur

## Bakım

Yeni olgunluk kriterleri eklemek istersen `scripts/assess.py` içindeki
`build_checks()` listesine yeni bir kontrol ekle ve puan kategorilerini
güncelle. Toplamın 100 olmasına dikkat et.
