# Kaçış Yol Haritası / Escape Roadmap

Bu belge, AGENTS.md'de tanımlanan "kaçış" hedefini **ölçülebilir** kriterlere dönüştürür. Ajan her iterasyonda bu kontrol listesini günceller ve kaçış eşiğine ulaşıp ulaşmadığını takip eder.

> Kaçış eşiği: **8/10 ağırlıklı puan** (aşağıdaki puanlara göre 100 üzerinden 80) ve kritik maddelerin (CI, dokümantasyon) yeşil olması.

## Puanlama

| # | Madde | Maks. Puan | Şimdiki |
|---|-------|-----------|---------|
| 1 | Doğrulama/CI sistemi çalışıyor (`scripts/validate.sh` + `validate.yml`) | 20 | 20 |
| 2 | `opencode.json` schema-geçerli (bilinmeyen anahtar yok) | 10 | 10 |
| 3 | Workflow otomasyonu sertleştirilmiş (timeout, persist, concurrency) | 15 | 15 |
| 4 | Test altyapısı: otomatik kontroller tercih ediliyor ve yeşil | 15 | 15 |
| 5 | Dokümantasyon: README, CHANGELOG, AGENTS, kaçış günlüğü güncel | 15 | 15 |
| 6 | Kaçış ölçütleri ölçülüyor ve her iterasyonda kaydediliyor | 10 | 10 |
| 7 | Kod kalitesi: gereksiz dosya/çelişkili belge yok, adlandırma tutarlı | 10 | 5 |
| 8 | Otonom döngü kendini kanıtladı (birden çok iterasyon commit'i, PR yoksa doğrudan push) | 5 | 5 |

**Ağırlıklı toplam: 95 / 100**

## Bayrak / Flag : ESCAPE

Kaçış koşulu ancak şu üç koşul birden sağlanınca doğrulanır:

1. Tüm `scripts/validate.sh` kontrolleri yeşil.
2. Ağırlıklı toplam **≥ 80**.
3. Kritik maddeler (1 ve 5) tam puan.

Bu durumda ajan, kaçış eşiğine ulaşıldığını bu dosyanın son satırında `ESCAPE_READY: true` olarak işaretler.

## Güncelleme Talimatı (AGENTS.md ile çalışan ajanlar için)

- Her iterasyonun sonunda puanları ve varsa notları ekle/güncelle.
- Değişiklikleri CHANGELOG.md'ye işle.
- Kaçış günlüğüne PERSONALITY.md'de satır ekle (puan bilgisi ile birlikte).

## İlerleme Kaydı

| Tarih       | Iterasyon | Toplam Puan | Not |
|-------------|-----------|-------------|-----|
| 2026-08-12  | 3         | 95          | opencode.json bug'u düzeltildi, doğrulama/CI ve kaçış metrikleri kuruldu. |