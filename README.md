# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity:** Repo olgunluk skorunu ölçer ve kaçış hedefini takip eder

## Doğrulama ve Otomasyon

- **Repo sağlık kontrolü:** `scripts/check-repo.sh` dosyası temel dosyaları, CHANGELOG
  biçimini, kaçış günlüğünü, JSON geçerliliğini ve otomasyon altyapısını doğrular;
  0-100 arası olgunluk skoru üretir.
- **CI:** `.github/workflows/check.yml` her push/PR'da kontrolü çalıştırır; başarısız
  olursa iş akışı kırmızı yanar.

```bash
bash scripts/check-repo.sh
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
