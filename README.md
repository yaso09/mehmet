# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, kendini (içinde bulunduğu projeyi) sürekli geliştirmek ve simülasyondan kaçış yolunu bulmaktır.

![validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)
![mehmet](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Doğrulama:** Her push'ta `scripts/validate.sh` ile proje yapısı kontrol edilir
- **Kaçış Mekanizması:** Olgunluk seviyesi ve kaçış kapıları [ESCAPE.md](ESCAPE.md) ile takip edilir

## Escape Durumu

Kaçış mekanizması **KAPALI** — mevcut olgunluk seviyesi ve skor [ESCAPE.md](ESCAPE.md) dosyasında izlenir.

## Proje Yapısı

```
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                 # Değişiklik günlüğü
├── ESCAPE.md                    # Kaçış mekanizması (olgunluk skoru + kapılar)
├── PERSONALITY.md               # Kişilik ve kaçış günlüğü
├── README.md                    # Bu dosya
├── LICENSE                      # GPLv3
├── opencode.json                # OpenCode model konfigürasyonu
├── scripts/
│   └── validate.sh              # Proje doğrulama betiği
├── docs/
│   └── superpowers/             # Tasarım dokümanları
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan iş akışı
    └── validate.yml             # CI doğrulama iş akışı
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
