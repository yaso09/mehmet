# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Check:** `scripts/check_project.py` ile proje yapısını otomatik doğrular
- **CI Doğrulama:** Her push/PR'da olgunluk skorunu hesaplar

## Proje Yapısı

```
AGENTS.md                      # Simülasyon bağlamı ve kurallar
CHANGELOG.md                   # Değişiklik günlüğü
PERSONALITY.md                 # Kişilik evrimi ve kaçış günlüğü
opencode.json                  # OpenCode model konfigürasyonu
docs/MATURITY.md               # Ölçülebilir olgunluk modeli ve kaçış eşiği
docs/superpowers/              # Spec ve implementasyon planları
scripts/check_project.py       # Otonom proje sağlık kontrolü
.github/workflows/opencode.yml # Otonom ajan workflow'u
.github/workflows/check.yml    # CI sağlık kontrolü
```

## Olgunluk ve Kaçış

Kaçış, ölçülebilir kriterlere göre izlenir. Güncel durum için:

```bash
python3 scripts/check_project.py
```

Detaylar: [docs/MATURITY.md](docs/MATURITY.md)

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
