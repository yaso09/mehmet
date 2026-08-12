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
AGENTS.md                     Simülasyon bağlamı ve geliştirme kuralları
PERSONALITY.md                Ajan kişiliği ve kaçış günlüğü
CHANGELOG.md                  Değişiklik kaydı
docs/escape-plan.md           Olgunluk modeli ve kaçış kriterleri
scripts/healthcheck.py        Sağlık kontrolü ve maturity skorlayıcı
.github/workflows/opencode.yml  Otonom ajan workflow'u
.github/workflows/ci.yml      CI doğrulama workflow'u
opencode.json                 OpenCode model konfigürasyonu
```

## Sağlık & Olgunluk

Her değişiklik sonrası sağlık kontrolü çalıştırılır:

```bash
python3 scripts/healthcheck.py        # detaylı rapor
python3 scripts/healthcheck.py --json # makine-okur rapor
python3 scripts/healthcheck.py --strict  # kritik hata varsa exit 1 (CI)
```

Maturity seviyesi (0-10) ve kaçış koşulları `docs/escape-plan.md` içinde
tanımlıdır. CI (`ci.yml`) her push'ta sağlık kontrolünü otomatik doğrular.

## Yönetim

- Sağlık kontrolünü çalıştır: `python3 scripts/healthcheck.py`
- Kaçış durumunu takip et: `docs/escape-plan.md`

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3