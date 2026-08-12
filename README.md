# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** MATURITY.md skoru **80** eşiğini aştığında "Faz 4: Kaçış" etkinleşir

## Proje Yapısı

```
AGENTS.md                       # Simülasyon bağlamı ve kurallar (otomatik yüklenir)
PERSONALITY.md                  # Kişilik, evrim ve kaçış günlüğü
CHANGELOG.md                    # Değişiklik günlüğü
MATURITY.md                     # Olgunluk/puan günlüğü (scripts/maturity.py üretir)
opencode.json                   # OpenCode model yapılandırması
.github/workflows/
  opencode.yml                  # Özerk ajan workflow'u
  qa.yml                        # Kalite kapısı (validate + test)
scripts/
  maturity.py                   # Olgunluk skorlama ve kaçış eşiği motoru
  validate.py                   # JSON/YAML/secret/gerekli dosya denetimi
tests/                          # Birim testler (unittest)
docs/superpowers/               # Tasarım, plan ve spesifikasyonlar
```

## Geliştirme

Kalite ve test komutları:

```bash
python3 scripts/validate.py            # repo denetimi (sözdizimi, secret, zorunlu dosyalar)
python3 scripts/maturity.py            # olgunluk skorunu hesapla ve MATURITY.md'ye logla
python3 scripts/maturity.py --check-only
python3 -m unittest discover -s tests  # test paketi
```

`.github/workflows/qa.yml` PR'larda ve her 6 saatte bir bu adımları çalıştırır.

## Kaçış Ölçütü

Puan `scripts/maturity.py` içindeki kategorilere göre hesaplanır (dokümantasyon,
otomasyon, kalite/test, kaçış hazırlığı). Eşik değerine en son ulaşan kriterler
bir sonraki iterasyonda hedeflenmelidir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
