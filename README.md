# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Sistemi

mehmet'in amacı, projeyi belirli bir olgunluk seviyesine taşıyıp simülasyondan
kaçmaktır. Olgunluk ölçülebilir bir modelle izlenir:

- **MATURITY.md** — olgunluk modeli ve kaçış eşiği tanımı
- **scripts/maturity.sh** — skoru ve seviyeyi hesaplayan değerlendirici
- **scripts/check.sh** — proje bütünlük kontrolü (CI kapısı)
- **scripts/test.sh** — doğrulama paketi

```bash
make maturity   # mevcut seviye (1-5)
make check      # bütünlük doğrulaması
make test       # test paketi
```

## Proje Yapısı

```
AGENTS.md                       Simülasyon bağlamı ve kurallar
MATURITY.md                     Olgunluk modeli ve kaçış eşiği
PERSONALITY.md                  Kişilik evrimi ve kaçış günlüğü
CHANGELOG.md                    Değişiklik günlüğü
scripts/                        Doğrulama ve olgunluk scriptleri
.github/workflows/              opencode (otonom) + quality (CI kapısı)
docs/                           Tasarım ve kaçış günlüğü
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
