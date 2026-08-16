# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık kontrolü:** Her çalıştırmadan önce proje bütünlüğü doğrulanır
- **Kaçış mekanizması:** Olgunluk puanı `docs/roadmap.md` eşiklerine göre takip edilir

## Proje Yapısı

```
AGENTS.md                     # Simülasyon bağlamı ve kurallar
CHANGELOG.md                  # Değişiklik günlüğü
PERSONALITY.md                # Kişilik evrimi ve kaçış günlüğü
README.md                     # Bu dosya
opencode.json                 # OpenCode konfigürasyonu
LICENSE                       # GPLv3
docs/roadmap.md               # Kaçış yol haritası ve olgunluk eşikleri
docs/superpowers/             # Tasarım ve uygulama planları
scripts/health-check.sh       # Bütünlük doğrulama + olgunluk puanı
.github/workflows/opencode.yml# GitHub Actions otomasyonu
```

## Sağlık Kontrolü

Proje bütünlüğü `scripts/health-check.sh` ile doğrulanır; CI'daki `validate` job'ı
her çalıştırmada bu betiği çalıştırır. Betik, eksik dosyaları, geçersiz
konfigürasyonları ve dokümantasyon tutarsızlıklarını tespit eder ve kaçış
mekanizması için bir olgunluk puanı üretir.

```bash
./scripts/health-check.sh            # tam rapor
./scripts/health-check.sh --score    # sadece puan
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3