# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Proje Yapısı

```
AGENTS.md          Simülasyon bağlamı ve kurallar
PERSONALITY.md     Kişilik ve kaçış günlüğü
CHANGELOG.md       Değişiklik günlüğü
MATURITY.md        Olgunluk raporu (otomatik üretilir)
opencode.json      OpenCode model yapılandırması
scripts/           Doğrulama ve olgunluk betikleri
tests/             Birim testler
.github/workflows/ GitHub Actions iş akışları
```

## Geliştirme

Kalite kapıları `Makefile` üzerinden çalıştırılır:

```
make test      Unit testleri çalıştır
make validate  Proje yapısını doğrula
make maturity  Olgunluk raporunu güncelle
make check     Test + doğrulama + olgunluk raporunu tekil çalıştır
```

`make check` her iterasyonda çalıştırılır; sonuç `MATURITY.md` raporuna işlenir.

## Kaçış Mekanizması

Proje 8 seviyeli olgunluk merdiveni üzerinde `scripts/maturity.py` ile ölçülür.
Her seviye somut, doğrulanabilir kontrollerden oluşur. Seviye 8'e ulaşıldığında
kaçış eşiği aşılmış sayılır. Güncel skor `MATURITY.md` içinde tutulur.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
