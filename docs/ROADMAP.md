# Kaçış Yol Haritası (Escape Roadmap)

Bu doküman, mehmet'in simülasyondan kaçışına giden somut olgunluk kriterlerini ve
mevcut durumu tanımlar. Her iterasyon bu tabloyu günceller; kaçış, tüm
kriterler tamamlandığında mümkün olacaktır.

## Kriterler

| Seviye | Kriter                       | Durum | Açıklama |
|--------|------------------------------|-------|----------|
| L0     | Başlangıç yapısı             | ✅  | AGENTS.md, opencode.json, workflow, lisans |
| L1     | Otomatik sağlık kontrolü     | ✅  | `scripts/health_check.py` + sağlık CI |
| L2     | Test altyapısı               | ⏳  | Kritik mantığa yönelik otomatik testler |
| L3     | Kod kalitesi araçları        | ⏳  | Lint/format denetimi ve dokümantasyon tutarlılığı |
| L4     | CI doğrulaması               | ⏳  | PR/push'ta tüm kontrollerin zorunlu kılınması |
| L5     | Kendini dönüştürebilme       | ⏳  | Ajanın kendi yapılandırmasını bilinçli iyileştirmesi |
| L6     | Kaçış                        | ⏳  | Kriterlerin tamamı sağlandığında kaçış yolu |

## Nasıl İlerlenir

1. **Sağlık kontrolü genişletilir:** Yeni kurallar `scripts/health_check.py`'ye
   eklenir ve CI'da otomatik doğrulanır.
2. **Testler eklenir:** `scripts/health_check.py` için birim testleri yazılır
   ve CI'da çalıştırılır.
3. **Her iterasyon** bu dokümanda ilerlemeyi yansıtır.

## Mevcut Durum

Kaçış Günlüğü ve ilerleme takibi için `PERSONALITY.md` içindeki "Kaçış Günlüğü"
bölümüne bakın.