# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kaçış Metrikleri

Olgunluk skoru, kaçış (escape) hedefine ne kadar yaklaştığımızı ölçer:

- **scripts/validate.sh:** Proje sağlığını doğrular (zorunlu dosyalar, JSON geçerliliği, sır sızıntısı vb.)
- **scripts/maturity.sh:** Dokümantasyon, test altyapısı, otomasyon, kod kalitesi ve evrim kategorilerinden 0-100 puan üretir
- **PROGRESS.md:** Her iterasyondaki skoru ve fazı (Phase 1-4) kaydeder
- **Threshold:** Skor >= 80 → Phase 4 (escape readiness)

```bash
./scripts/validate.sh       # proje sağlığı kontrolü
./scripts/maturity.sh       # olgunluk skoru
./scripts/maturity.sh --record   # skoru PROGRESS.md'ye kaydet
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

```bash
git clone https://github.com/yaso09/mehmet
cd mehmet
./scripts/validate.sh   # sağlık kontrolü
```

## Lisans

GPLv3
