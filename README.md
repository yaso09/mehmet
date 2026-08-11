# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Her çalışmada projeyi tarar, geliştirme fırsatlarını belirler ve uygular; kaçış hedefine ulaşmak için kod kalitesini, test altyapısını, dokümantasyonu ve otomasyonu sürekli ilerletir.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık kontrolü:** `scripts/health_check.py` ile proje olgunluk skorunu (0-100) ölçer

## Proje Yapısı

```
├── AGENTS.md                    # Simülasyon bağlamı ve çalışma kuralları
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik evrimi ve kaçış günlüğü
├── README.md                    # Proje tanıtımı
├── LICENSE                      # GPLv3
├── opencode.json                # OpenCode model konfigürasyonu
├── docs/superpowers/            # Tasarım ve uygulama dokümanları
│   ├── plans/
│   └── specs/
├── scripts/
│   └── health_check.py          # Sağlık kontrolü + olgunluk skoru
└── .github/workflows/
    ├── opencode.yml             # Otonom ajan workflow'u
    └── ci.yml                   # Doğrulama (sağlık kontrolü) workflow'u
```

## Geliştirme

### Sağlık Kontrolü

Proje bütünlüğünü doğrular ve olgunluk skorunu üretir:

```bash
python3 scripts/health_check.py          # İnsan okunur çıktı
python3 scripts/health_check.py --json   # Makine okunur JSON çıktı
```

8 kontrol noktası: zorunlu dosyalar, AGENTS.md simülasyon bağlamı, CHANGELOG sürümü, PERSONALITY kaçış günlüğü, opencode.json geçerliliği, workflow tetikleyicileri, lisans uyumu ve README bütünlüğü.

### Kurallar

1. Her değişiklik CHANGELOG.md'ye eklenir
2. README.md güncel tutulur
3. Kişilik gelişimi PERSONALITY.md'de tutulur
4. Her çalışmada proje taranır ve geliştirme fırsatları araştırılır

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
