# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur; `quality-gate` ile otomatik doğrulama talep eder
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Olgunluk takibi:** `bash scripts/verify.sh --score` ile kaçış eşiğini izler

## Doğrulama

Proje sağlığı ve olgunluk puanı otomatik doğrulanır:

```bash
bash scripts/verify.sh            # yapısal + içerik kontrolü ve puan
bash scripts/verify.sh --update   # puanı MATURITY.md tablosuna yazar
bash tests/test_project.sh        # test harness
```

CI (`quality-gate` job'u) PR'larda bu komutları zorunlu kılar.

## Mimari

Yapı `/docs/superpowers/specs/` içindeki tasarım dokümanında açıklanır. Olgunluk/kaçış koşulları `MATURITY.md`'dedir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
