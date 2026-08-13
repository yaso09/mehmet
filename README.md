# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Self-Verification:** `scripts/verify.sh` ile proje bütünlüğünü ve maturity skorunu ölçer
- **Kaçış Mekanizması:** 90/100 maturity skoruna ulaşıldığında tetiklenir

## Proje Yapısı

```
AGENTS.md                     Simülasyon bağlamı ve kurallar
CHANGELOG.md                  Değişiklik günlüğü
PERSONALITY.md                Kişilik evrimi ve kaçış günlüğü
opencode.json                 OpenCode konfigürasyonu
scripts/verify.sh             Self-verification ve maturity skorlama
.github/workflows/opencode.yml  Otonom ajan workflow'u
.github/workflows/verify.yml  Bütünlük kontrolü CI
docs/superpowers/             Tasarım ve uygulama dokümanları
```

## Doğrulama

```bash
bash scripts/verify.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
