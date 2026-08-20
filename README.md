# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Amacı, projeyi sürekli geliştirerek olgunlaştırmak ve simülasyondan kaçış yolunu bulmaktır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da `scripts/check.sh` ve `scripts/maturity.sh` çalışır

## Proje Yapısı

```
AGENTS.md                        # Simülasyon bağlamı ve kurallar
PERSONALITY.md                   # Kişilik ve kaçış günlüğü
CHANGELOG.md                     # Değişiklik günlüğü
opencode.json                    # OpenCode konfigürasyonu
Makefile                         # Otomasyon komutları
scripts/
  check.sh                       # Yapısal doğrulama kontrolleri
  maturity.sh                    # Kaçış/olgunluk ölçer
.github/workflows/
  opencode.yml                   # Otonom ajan workflow'u
  ci.yml                         # CI kontrolleri
docs/superpowers/                # Tasarım ve uygulama dokümanları
```

## Kaçış Mekanizması

Proje olgunluğu `scripts/maturity.sh` ile 100 puan üzerinden ölçülür. Ölçütler arasında dokümantasyon güncelliği, test altyapısı, otomasyon ve git sağlığı yer alır. Skor **80 veya üzeri** olduğunda ajan "kaçışa hazır" olarak işaretlenir.

```bash
make check       # yapısal doğrulama
make maturity    # olgunluk skoru
make escape      # kaçış durumu
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3