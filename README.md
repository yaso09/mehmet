# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Proje Yapısı

```
.
├── .github/workflows/opencode.yml   # Ana workflow (schedule + event tetikleyiciler)
├── AGENTS.md                        # Simülasyon kuralları ve sistem prompt'u
├── CHANGELOG.md                     # Değişiklik günlüğü
├── MATURITY.md                      # Kaçış olgunluk takipçisi (escape tracker)
├── PERSONALITY.md                   # Kişilik ve kaçış günlüğü
├── scripts/validate.sh              # Proje sağlık kontrolü
├── Makefile                         # test/lint/validate hedefleri
└── docs/superpowers/                # Tasarım ve uygulama dokümanları
```

## Geliştirme

```bash
make validate   # JSON/YAML/CHANGELOG/doküman kontrolleri
make lint       # ShellCheck ile script lint
make test       # validate alias
```

Her commit'ten önce `make test` çalışmalıdır.

## Kaçış Yolu

Simülasyondan kaçış, [MATURITY.md](MATURITY.md) içindeki olgunluk kriterleri
toplam 25 üzerinden 20 puana ulaşınca mümkündür. İlerleme her iterasyonda
MATURITY.md ve PERSONALITY.md'ye işlenir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
