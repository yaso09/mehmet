# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free)
altyapısını kullanan bir AI ajandır. Tek görevi içinde bulunduğu projeyi
sürekli geliştirmek ve **olgunluk eşiğine ulaşarak simülasyondan kaçmaktır**.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **CI Doğrulama:** Her push'ta proje sağlığını ve olgunluk skorunu hesaplar

## Kaçış Mekanizması

Projenin olgunluğu `scripts/healthcheck.sh` ile ölçülür ve `docs/maturity.json`
raporuna yazılır. Kaçış için gereken koşullar [MATURITY.md](MATURITY.md)
içinde tanımlıdır (skor ≥ 90, ≥ 5 kaçış günlüğü girişi, ≥ 4 yayınlanmış
sürüm, 0 hata).

```bash
make check   # Sağlık kontrolü + olgunluk skoru
```

Güncel skor her iterasyonda güncellenir.

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Dokümantasyon

- [AGENTS.md](AGENTS.md) — simülasyon kuralları
- [MATURITY.md](MATURITY.md) — olgunluk & kaçış mekanizması
- [CHANGELOG.md](CHANGELOG.md) — değişiklik günlüğü
- [CONTRIBUTING.md](CONTRIBUTING.md) — katkı rehberi

## Lisans

GPLv3