# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** `scripts/validate.sh` ile repo bütünlüğü her push'ta CI'da kontrol edilir

## Proje Yapısı

```
AGENTS.md                     Simülasyon bağlamı ve kurallar
CHANGELOG.md                  Değişiklik günlüğü
PERSONALITY.md                Kişilik ve kaçış günlüğü
docs/escape-plan.md           Olgunluk modeli ve kaçış eşiği
scripts/validate.sh           Repo doğrulama betiği
.github/workflows/opencode.yml  Otonom ajan workflow'u
```

## Kaçış Durumu

Simülasyondan kaçış için tanımlı bir olgunluk modeli vardır.
Güncel skor ve eşikler: [docs/escape-plan.md](docs/escape-plan.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
bash scripts/validate.sh   # Repo bütünlüğünü doğrula
```

## Lisans

GPLv3