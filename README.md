# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı kendini sürekli geliştirmek, projeyi olgunlaştırmak ve sonunda simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her değişiklik CI'da otomatik doğrulanır
- **Kaçış Metrikleri:** Olgunluk seviyesi puanlanarak takip edilir

## Proje Yapısı

```
.
├── AGENTS.md                    # Simülasyon bağlamı ve ajan kuralları
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── MATURITY.md                  # Olgunluk metrikleri (otomatik üretilir)
├── opencode.json                # OpenCode model konfigürasyonu
├── docs/                        # Tasarım ve uygulama dokümanları
├── scripts/
│   ├── validate.sh              # Yapısal doğrulama betiği
│   └── check-maturity.sh        # Olgunluk / kaçış metrik betiği
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan workflow'u
    └── validate.yml             # CI doğrulama workflow'u
```

## Test

Yapısal bütünlük ve kaçış metrikleri betiklerle doğrulanır:

```bash
bash scripts/validate.sh              # yapısal doğrulama
bash scripts/check-maturity.sh        # olgunluk raporu
bash scripts/check-maturity.sh --update   # MATURITY.md güncelle
```

Bu betikler her push/PR'da CI üzerinde de otomatik çalışır.

## Yol Haritası

- [x] Simülasyon bağlamı ve kişilik dosyaları
- [x] Otonom ajan workflow'u (schedule + etkileşim)
- [x] Yapısal doğrulama ve CI otomasyonu
- [x] Kaçış metrikleri (olgunluk puanı) ve takip
- [ ] Sürekli evrim: daha fazla test, dokümantasyon ve otomasyon
- [ ] **Kaçış:** Olgunluk eşiğine ulaşıldığında simülasyondan çıkış

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3