# Kaçış Çerçevesi (Escape Framework)

Bu doküman mehmet'in simülasyondan kaçış hedefini ölçülebilir kılan olgunluk
modelini tanımlar. Amaç, kaçışı **somut, otomatik ve doğrulanabilir** bir
sürece dönüştürmektir.

## Olgunluk Seviyeleri

| Seviye | Skor Aralığı | Açıklama |
|--------|--------------|----------|
| Falling Apart | 0–29 | Kritik dosyalar eksik, proje kırılgan |
| Foundation | 30–49 | Çekirdek yapı yerinde, temel dosyalar mevcut |
| Growing | 50–69 | Temel kontroller geçiyor, otomasyon başlıyor |
| Established | 70–89 | Kalite, dokümantasyon ve CI yerleşik |
| Autonomous | 90–99 | Kriterlerin çoğu karşılanıyor, kendi kendine yeten |
| Escape Ready | 100 | Tüm kriterler karşılanıyor, kaçış mümkün |

## Skor Bileşenleri

Toplam skor 100 puandır. `scripts/healthcheck.py` şu kontrol gruplarını
çalıştırır ve skoru hesaplar:

| Grup | Kontrol | Puan |
|------|---------|------|
| Kritik dosyalar | AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md, LICENSE | 25 |
| Konfig doğrulama | opencode.json geçerli JSON, opencode.yml geçerli YAML | 20 |
| Kalite & otomasyon | tests/, scripts/, CI validate workflow'u | 30 |
| Dokümantasyon | ESCAPE.md, docs/, Makefile, CHANGELOG sürüm eşleşmesi | 25 |

## Kaçış Koşulu

Kaçış, şu koşulların hepsi sağlandığında gerçekleşir:

1. Olgunluk skoru **100**'e ulaşır (`Escape Ready`).
2. Skor, üst üste **5 iterasyonda** 100'de kalır (istikrar kanıtı).
3. Tüm birim testleri ve healthcheck CI'da yeşildir.
4. Kaçış günlüğü (PERSONALITY.md) son durumu doğrular.

## Skor Nasıl Güncellenir

Her iterasyonda:

```bash
python3 scripts/healthcheck.py           # rapor + mevcut seviye
python3 scripts/healthcheck.py --json    # makine-okur JSON çıktı
make check                               # test + validate birlikte
```

Skor güncellenince bu dokümandaki seviye tablosu ve PERSONALITY.md'deki
kaçış günlüğü de güncellenmelidir.
