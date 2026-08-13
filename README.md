# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Sağlık Kontrolü:** Her çalıştırmada testler ve olgunluk skoru otomatik doğrulanır

## Kaçış Mekanizması

`scripts/project_health.py` projenin olgunluğunu 0-100 arası ölçer. Skor
`ESCAPE_THRESHOLD` (80) değerine ulaştığında proje kaçışa hazır kabul edilir.

```bash
make health   # insan-okur rapor
make score    # sadece skor
make json     # JSON rapor
```

## Proje Yapısı

```
AGENTS.md                       # Simülasyon prompt'u (opencode tarafından otomatik okunur)
CHANGELOG.md                    # Değişiklik günlüğü
PERSONALITY.md                  # Kişilik evrimi ve kaçış günlüğü
docs/superpowers/               # Tasarım dokümanları
scripts/project_health.py       # Olgunluk/sağlık ölçer
scripts/test_project_health.py  # Birim testleri
Makefile                        # test/health/score/json/clean hedefleri
opencode.json                   # Model konfigürasyonu
.github/workflows/opencode.yml  # CI workflow
```

## Geliştirme

```bash
make test     # birim testlerini çalıştır
make health   # olgunluk kontrolü
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
