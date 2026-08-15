# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Projeyi sürekli tarar, geliştirme fırsatlarını tespit eder, kod kalitesini artırır ve kaçış olgunluğunu ölçer.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Tarama:** Proje kökünü analiz edip geliştirme fırsatlarını listeler
- **Olgunluk (Maturity):** Kaçış eşiğine (0.90) göre ilerlemeyi skorlar

## Yapı

```
mehmet/
  maturity.py   # Kaçış olgunluğu skorlama motoru
  scanner.py    # Proje tarama ve fırsat tespiti
  report.py     # Komut satırı raporu
  __main__.py   # python -m mehmet giriş noktası
tests/          # pytest testleri
docs/           # tasarım ve plan dokümanları
```

## Kullanım

```bash
python -m mehmet            # mevcut dizini tara ve raporla
python -m mehmet /path      # belirli bir dizini tara
```

## Geliştirme

```bash
pip install -e . pytest
pytest
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3