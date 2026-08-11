# Maturity / Olgunluk Sistemi

Bu proje, **kaçış** hedefi için somut, ölçülebilir bir olgunluk sistemine sahiptir.
Her iterasyonda `scripts/selfcheck.py` bu metriği hesaplar ve CI'da raporlar.

## Kaçış Eşiği (Escape Threshold)

- Skor **80/100 veya üzeri**: olgunluk eşiği aşıldı, kaçış yolu hazır.
- Skor **40-79**: iyi durumda, geliştirmeye devam.
- Skor **40 altı**: kırılgan, kritik düzeltmeler gerekli. CI bunu build hatası olarak işaretler.

## Skor Kategorileri

| Kategori | Puan | Açıklama |
|---|---|---|
| Yapı | 25 | Çekirdek dosyalar, docs/, .gitignore |
| Konfigürasyon | 20 | opencode.json geçerliği, workflow yapısı, concurrency |
| Dokümantasyon | 25 | README bölümleri, CHANGELOG sürümleri, kaçış günlüğü |
| Otomasyon | 20 | schedule, manuel tetikleme, selfcheck'in CI'da çalışması |
| Testler | 10 | scripts/selfcheck.py varlığı ve çalışabilirliği |

Toplam: **100 puan**.

## Kullanım

```bash
python3 scripts/selfcheck.py
```

CI'da `selfcheck` işi her tetikleyicide bu aracı çalıştırır; `autonomous` ve `comment`
işleri onun başarısını bekler.

## Amacı

- Projenin ilerlemesini objektif olarak ölçmek.
- Kaçış hedefine (olgunluk) doğru somut adımlar atmak.
- Gerilemeyi erken yakalamak (kalite kapısı / quality gate).