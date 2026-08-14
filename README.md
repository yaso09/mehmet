# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** [MATURITY.md](MATURITY.md) olgunluk skorunu izler, ≥ 90/100 eşiğinde tetiklenir
- **Otomatik Doğrulama:** `scripts/validate.py` proje bütünlüğünü her push/PR'da CI üzerinden doğrular

## Yapı

```
AGENTS.md                        Simülasyon bağlamı ve kurallar
PERSONALITY.md                   Kişilik evrimi ve kaçış günlüğü
MATURITY.md                      Olgunluk skoru ve kaçış eşiği
CHANGELOG.md                     Değişiklik günlüğü
opencode.json                    OpenCode model konfigürasyonu
scripts/validate.py              Proje bütünlük doğrulayıcısı
.github/workflows/opencode.yml   Otonom ajan workflow'u
.github/workflows/ci.yml         Doğrulama CI workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
