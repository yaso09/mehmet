# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Otomasyon:** Her tetiklemede testler ve olgunluk metrikleri otomatik çalışır

## Olgunluk ve Kaçış Mekanizması

Kaçış, projenin sürdürülebilir tam olgunluğa ulaşmasıyla gerçekleşir. Olgunluk
skoru `scripts/maturity.py` ile 4 boyutta ölçülür: dokümantasyon, otomasyon,
test ve meta. Kaçış yalnızca skor 100/100'e ulaştığında ve bu skor ardışık
3 iterasyon boyunca korunduğunda sağlanır. Güncel durum `MATURITY.md` dosyasında
takip edilir.

```bash
python3 scripts/maturity.py              # skoru görüntüle
python3 scripts/maturity.py --update     # skoru MATURITY.md'ye yaz
python3 scripts/maturity.py --json       # JSON çıktı
```

## Testler

Proje bütünlüğü testleri `tests/` dizininde, standart kütüphane (`unittest`)
ile yazılmıştır. Ek bağımlılık gerekmez.

```bash
python3 -m unittest discover -s tests -v
```

Testler ve olgunluk metrikleri her workflow tetiklemesinde `check` job'ı
tarafından otomatik çalıştırılır.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Lisans

GPLv3