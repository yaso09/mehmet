# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

**Mevcut sürüm: 0.3.0**

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI:** Her push/PR'da proje bütünlüğünü doğrular (`scripts/validate.sh`)

## Proje Yapısı

```
.
├── .github/workflows/    # GitHub Actions (opencode + ci)
├── docs/                 # Tasarım ve plan dokümanları
├── scripts/              # Doğrulama ve bakım scriptleri
├── AGENTS.md             # Simülasyon kuralları (system prompt)
├── CHANGELOG.md          # Değişiklik günlüğü
├── PERSONALITY.md        # Kişilik evrimi ve kaçış günlüğü
├── opencode.json         # OpenCode model konfigürasyonu
└── LICENSE               # GPLv3
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Testleri ve proje bütünlüğünü doğrulamak için:

```bash
./scripts/validate.sh
```

## Lisans

GPLv3