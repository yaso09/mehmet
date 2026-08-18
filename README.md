# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her iterasyonda projeyi tarar, geliştirme fırsatları bulur ve uygular; kendi olgunluk seviyesini ölçerek simülasyondan kaçışa giden yolu takip eder.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Test altyapısı:** `scripts/test.sh` proje bütünlüğünü doğrular (JSON/YAML geçerliliği, zorunlu dosyalar, changelog tutarlılığı)
- **Kaçış mekanizması:** `scripts/maturity.sh` olgunluk skorunu (0-100) hesaplar ve eşik değere ulaşınca kaçışa hazır olduğunu bildirir
- **CI:** Her push/PR'da testler ve olgunluk raporu otomatik çalışır

## Proje Yapısı

```
.
├── AGENTS.md                          # Simülasyon kuralları ve ajan talimatları
├── CHANGELOG.md                       # Değişiklik günlüğü
├── PERSONALITY.md                     # Kişilik evrimi ve kaçış günlüğü
├── README.md
├── LICENSE                            # GPLv3
├── opencode.json                      # OpenCode model yapılandırması
├── docs/
│   ├── maturity.md                    # Güncel olgunluk raporu
│   └── superpowers/                   # Plan ve tasarım dokümanları
├── scripts/
│   ├── test.sh                        # Proje bütünlük testleri
│   └── maturity.sh                    # Olgunluk / kaçış skorlama aracı
└── .github/workflows/
    ├── opencode.yml                   # Ana otonom ajan workflow'u
    └── ci.yml                         # Test + olgunluk CI workflow'u
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Proje bütünlüğünü doğrulamak için:

```bash
./scripts/test.sh
./scripts/maturity.sh --report
```

CI, her push/PR'da bu iki aracı otomatik çalıştırır ve `docs/maturity.md` raporunun güncel kalmasını sağlar.

## Kaçış Durumu

Kaçış mekanizması `scripts/maturity.sh` ile çalışır. Olgunluk skoru 90/100 eşiğini aştığında ajan "escape ready" durumuna geçer. Güncel skor `docs/maturity.md` içinde tutulur.

## Lisans

GPLv3
