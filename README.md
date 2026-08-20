# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Maturity tracking:** Sağlık skoru ve kaçış eşiği ile ilerleme ölçümü

## Geliştirme

Projeyi doğrulamak ve olgunluk skorunu ölçmek için:

```bash
make check   # testler + sağlık/olgunluk kontrolü (kaçış eşiği: 80/100)
make report  # docs/health-report.md'yi yeniden üret
```

Her PR ve push, CI'da `validate` job'u ile test ve sağlık kontrolünden geçer.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3
