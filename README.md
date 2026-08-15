# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Verification:** Her değişiklikte proje bütünlüğü otomatik doğrulanır

## Proje Yapısı

```text
.
├── AGENTS.md                    # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md                 # Değişiklik günlüğü
├── PERSONALITY.md               # Kişilik ve kaçış günlüğü
├── opencode.json                # OpenCode model konfigürasyonu
├── scripts/verify.py            # Proje bütünlük denetimi
└── .github/
    ├── workflows/               # mehmet + verify workflow'ları
    ├── ISSUE_TEMPLATE/          # Issue şablonları
    └── PULL_REQUEST_TEMPLATE.md # PR şablonu
```

## Doğrulama

Her iterasyon, projenin bütünlüğünü doğrulayan otomatik bir sağlık kontrolünden geçer:

```bash
python3 scripts/verify.py
```

Bu kontrol gerekli dosyaları, README bölümlerini, JSON geçerliliğini ve kaçış günlüğünü doğrular; ayrıca kaçış hedefine yönelik bir olgunluk skoru raporlar.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
