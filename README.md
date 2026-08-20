# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Escape:** Olgunluk skorunu takip eder ve kaçış eşiğine ulaşmayı hedefler

## Kaçış Mekanizması

mehmet, simülasyondan kaçmak için olgunluk seviyesine ulaşmalıdır. Skor
dokümantasyon, kod, otomasyon ve kalite boyutlarında 0–100 arasında ölçülür.
Kriterler `docs/ESCAPE.md`'de, ölçüm `scripts/escape_score.py`'de tanımlıdır.

```bash
make score    # mevcut puanı göster
make test     # pytest çalıştır
make verify   # proje sağlık kontrolü
```

## Proje Yapısı

```
├── .github/workflows/opencode.yml   # otomasyon + verify job
├── docs/ESCAPE.md                   # kaçış kriterleri
├── scripts/escape_score.py          # olgunluk skoru
├── scripts/verify_project.py        # sağlık kontrolü
└── tests/                           # pytest testleri
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
