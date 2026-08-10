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

## Gelişim Durumu (Maturity)

mehmet, kaçış hedefine doğru ölçülebilir ilerler. Olgunluk skoru her iterasyonda
`scripts/verify.py` ile hesaplanır ve `docs/escape-plan.md` içindeki kriterlere göre
değerlendirilir.

| Durum | Değer |
|-------|-------|
| Olgunluk skoru | 100/100 (2026-08-10) |
| Kaçış eşiği | ≥ 90/100 ve kritik hata yok |

Doğrulamayı yerel olarak çalıştırmak için:

```bash
python3 scripts/verify.py       # ayrıntılı rapor
python3 scripts/verify.py --json  # JSON çıktısı
```

## Lisans

GPLv3
