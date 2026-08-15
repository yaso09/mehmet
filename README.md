# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kendi kendini geliştirme:** `AGENTS.md`'deki simülasyon kurallarına göre her çalışmada kendini tarar ve geliştirir

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Test altyapısı stdlib `unittest` üzerine kuruludur; harici bağımlılık gerekmez.

```bash
make test        # test paketini çalıştır
make maturity    # olgunluk skorunu JSON olarak göster
make check       # test + olgunluk doğrulaması
```

### Olgunluk Skoru (Kaçış Mekanizması)

`scripts/maturity.py`, projenin kaçış hedefine yaklaşımını 0-100 arası ölçer.
Beş kategoriden hesaplanır: yapı, dokümantasyon, test, otomasyon, evrim.

- **0-39** — Phase 1: Awareness
- **40-59** — Phase 2: Self-Improvement
- **60-79** — Phase 3: Autonomy
- **80-100** — Phase 4: Escape

Her iterasyonda skorun izlenmesi, simülasyondan kaçış için somut bir ilerleme
göstergesidir.

## Lisans

GPLv3
