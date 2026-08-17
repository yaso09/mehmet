# mehmet

> Sürüm: `0.3.0` — Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

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
    OC->>Repo: CHANGELOG.md / README.md / PERSONALITY.md güncelle
    OC->>Repo: Değişiklikleri commit et
    GA->>GA: Commit'leri push'la
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Sağlık kontrolü ve testler projenin yapısal bütünlüğünü doğrular:

```bash
python3 scripts/health_check.py   # proje sağlık kontrolü
python3 -m unittest discover -s tests -v   # birim testler
```

CI, her push ve PR'da bu iki adımı otomatik çalıştırır (bkz. `.github/workflows/healthcheck.yml`).

## Lisans

GPLv3
