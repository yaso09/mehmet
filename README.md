# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Kalite Kontrol

Proje bütünlüğü `make check` ile doğrulanır (bağımlılıksız, saf Python):

```bash
make check
```

Bu kontrol her push ve PR'da CI (`validate.yml`) tarafından zorunlu tutulur.

## Olgunluk Takibi

Kaçış hedefi docs/MATURITY.md'deki 6 seviyeli olgunluk modeline göre
ölçülür. Mevcut seviye ve ilerleme yolu orada listelenir; her iterasyon
PERSONALITY.md'deki kaçış günlüğüne kaydedilir.

## Lisans

GPLv3
