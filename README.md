# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Proje Yapısı

| Dosya / Dizin | Açıklama |
|---|---|
| `AGENTS.md` | Simülasyon bağlamı ve kaçış mekanizması kuralları |
| `CHANGELOG.md` | Değişiklik günlüğü (her iterasyonda güncellenir) |
| `PERSONALITY.md` | Ajanın kişiliği ve kaçış günlüğü |
| `MATURITY.md` | Olgunluk skoru (kaçış mekanizması çıktısı) |
| `scripts/maturity.sh` | Olgunluk ölçüm betiği |
| `tests/run_tests.sh` | Yapısal bütünlük testleri |
| `Makefile` | `make test`, `make maturity`, `make check` |
| `docs/` | Tasarım ve uygulama dokümanları |
| `opencode.json` | OpenCode konfigürasyonu |

## Kaçış Mekanizması

Proje, `scripts/maturity.sh` ile ölçülen olgunluk seviyesine göre değerlendirilir:

- Skor **100 üzerinden** hesaplanır; **eşik 80 puandır**
- Eşiğe ulaşıldığında proje **kaçış aşamasına** (escape) geçer
- Güncel skor `MATURITY.md` içinde tutulur

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
make test      # yapısal bütünlük testleri
make maturity  # olgunluk skorunu güncelle
make check     # ikisini birden çalıştır
```

## Lisans

GPLv3