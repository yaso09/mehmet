# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Validation:** Her çalıştırmada `scripts/validate.sh` repo sağlığını kontrol eder
- **Olgunluk Takibi:** `scripts/maturity.sh` kaçış puanını (0-100) hesaplar; `PROGRESS.md`'de takip edilir

## Geliştirme / Doğrulama

```bash
# Repo sağlık kontrolü (zorunlu dosyalar, JSON geçerliliği, doküman bütünlüğü)
bash scripts/validate.sh

# Olgunluk / kaçış puanı
bash scripts/maturity.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Proje Yapısı

```
AGENTS.md                     # Simülasyon prompt'u
PERSONALITY.md                # Kişilik ve kaçış günlüğü
PROGRESS.md                   # Olgunluk takibi ve kaçış mekanizması
CHANGELOG.md                  # Değişiklik günlüğü
opencode.json                 # OpenCode konfigürasyonu
scripts/validate.sh           # Repo sağlık kontrolü
scripts/maturity.sh           # Olgunluk puanı hesaplayıcı
.github/workflows/opencode.yml # CI/otomasyon workflow'u
```

## Lisans

GPLv3
