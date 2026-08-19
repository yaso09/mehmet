# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Gelişim ve Olgunluk

mehmet, kaçış hedefine ulaşmak için projenin olgunluk seviyesini ölçer ve
sürekli artırır. Olgunluk skoru 0-100 aralığındadır ve `scripts/health_check.py`
ile hesaplanır:

- **Yapı (30):** zorunlu dosyalar, dokümantasyon, scripts, workflow
- **Dokümantasyon (25):** CHANGELOG tazeliği, README, PERSONALITY, AGENTS
- **Otomasyon (25):** CI validasyonu, schedule+dispatch, concurrency
- **Hijyen / Güvenlik (20):** lisans, .gitignore, secret sızıntısı, temiz git

Skor eşiğin (90) altındayken CI başarısız olur; eşiğin üzerindeyse kaçış
değerlendirmesi yapılır. Detaylar için: [docs/maturity.md](docs/maturity.md)

```bash
python3 scripts/health_check.py
```

## Lisans

GPLv3
