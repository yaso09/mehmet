# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda kendini geliştirir, test altyapısını büyütür ve kaçış (escape) hedefine doğru ilerler.

## Olgunluk / Kaçış Durumu

Kaçış, projenin olgunluk skorunun **80/100** eşiğini geçmesiyle mümkün olur. Güncel skor `scripts/maturity.py` ile hesaplanır:

```
python scripts/maturity.py .
```

Detaylar: [docs/escape-mechanism.md](docs/escape-mechanism.md)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Validate:** Testler ve olgunluk skoru her çalıştırmada doğrulanır
- **Kaçış Mekanizması:** Objektif olgunluk ölçümü ile simülasyondan çıkış yolu

## Proje Yapısı

```
├── .github/workflows/opencode.yml   # CI + otonom ajan workflow'u
├── scripts/maturity.py              # Olgunluk skoru hesaplayıcı
├── tests/                           # Test altyapısı (unittest)
├── AGENTS.md                        # Simülasyon kuralları
├── PERSONALITY.md                   # Kişilik ve kaçış günlüğü
├── CHANGELOG.md                     # Değişiklik günlüğü
└── docs/                            # Tasarım ve kaçış mekanizması dokümanları
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
python -m unittest discover -s tests   # testleri çalıştır
python scripts/maturity.py .           # olgunluk skorunu hesapla
```

## Lisans

GPLv3