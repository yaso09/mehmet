# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Audit:** `scripts/audit.py` projenin olgunluk seviyesini ölçer ve kaçış eşiğini izler

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Olgunluk denetimini yerel olarak çalıştır:

```bash
python3 scripts/audit.py
```

Betik; config geçerliliği, dokümantasyon, otomasyon ve test altyapısını
14 puan üzerinden değerlendirir. Skor 11.0 eşiğini aştığında kaçış
mekanizması tetiklenmiş sayılır ve rapor `.wellness` dosyasına yazılır.

## Dokümantasyon

Tasarım (design) ve uygulama planı `docs/superpowers/` altındadır.

## Lisans

GPLv3
