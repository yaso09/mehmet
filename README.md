# mehmet

Kendi kendisini geliştiren otonom AI ajan.

![Workflow: mehmet](https://github.com/yaso09/mehmet/actions/workflows/opencode.yml/badge.svg)
![Workflow: validate](https://github.com/yaso09/mehmet/actions/workflows/validate.yml/badge.svg)
![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Maturity](https://img.shields.io/badge/maturity-39%2F100-orange.svg)

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Autonomous:** Kendi kaçış günlüğünü tutar ve olgunluk skorunu takip eder

## Mimari

```mermaid
sequenceDiagram
    participant GA as GitHub Actions
    participant OC as OpenCode Agent
    participant Repo as Repository

    GA->>OC: Event tetiklendi (schedule/issue/PR)
    OC->>Repo: AGENTS.md oku (simülasyon bağlamı)
    OC->>Repo: Projeyi tara, mevcut durumu analiz et
    OC->>OC: DeepSeek V4 Flash Free (Zen) ile yanıt üret
    OC->>Repo: Dosyaları oku/yaz/düzenle
    OC->>Repo: CHANGELOG.md ve maturity.json güncelle
    OC->>Repo: Değişiklikleri commit et
    GA->>GA: Commit'leri push'la
```

## Proje Yapısı

```
mehmet/
├── .github/workflows/
│   ├── opencode.yml    # Ana otonom ajan workflow'u
│   └── validate.yml    # YAML/JSON doğrulama (test altyapısı)
├── docs/superpowers/   # Tasarım ve uygulama dokümanları
├── scripts/
│   └── validate.sh     # Depo doğrulama scripti
├── AGENTS.md           # Simülasyon bağlamı (system prompt)
├── CHANGELOG.md        # Değişiklik günlüğü
├── maturity.json       # Kaçış olgunluk takipçisi
├── PERSONALITY.md      # Ajan kişiliği ve kaçış günlüğü
└── opencode.json       # OpenCode model konfigürasyonu
```

## Kaçış Mekanizması

mehmet'in simülasyondan kaçışı, projenin olgunluk skoru `maturity.json` üzerinden takip edilir:

- **Code Quality:** Kod/yapılandırma kalitesi ve doğrulama kapsamı
- **Test Infrastructure:** CI/test altyapısının varlığı ve güvenilirliği
- **Documentation:** Dokümantasyon derinliği ve güncelliği
- **Automation:** Otomasyon seviyesi ve iş akışı sağlamlığı

Toplam skor `escape_threshold` değerine ulaştığında kaçış mümkün olur. Güncel skor ve gereksinimler `maturity.json` içinde listelenir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3