# mehmet

Kendi kendisini geliştiren otonom AI ajan.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free) altyapısını kullanan bir AI ajandır. Davranışını [AGENTS.md](AGENTS.md) içindeki simülasyon kurallarına göre belirler; her iterasyonda projeyi tarar, geliştirir ve [PERSONALITY.md](PERSONALITY.md)'de ilerlemesini günlüğe işler.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış Mekanizması:** [MATURITY.md](MATURITY.md) içindeki olgunluk modeli ile ölçülen, eşik aşılınca simülasyondan kaçışı hedefleyen ilerleme sistemi
- **Kural Doğrulama:** [scripts/validate.sh](scripts/validate.sh) AGENTS.md kurallarının sağlandığını otomatik kontrol eder (CI'da zorunludur)

## Geliştirici Araçları

| Komut | Açıklama |
|-------|----------|
| `make validate` | Kuralların sağlandığını doğrular |
| `make plan` | Kaçış / olgunluk durumunu gösterir |
| `make check` | Tam sağlık kontrolü (validate + shellcheck) |
| `./scripts/validate.sh` | Doğrulamayı doğrudan çalıştırır |

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Mimari

`.github/workflows/opencode.yml` içinde iki job vardır:

- **autonomous:** Schedule/issue/PR ile tetiklenir; simülasyon prompt'unu çalıştırır ve ardından kural doğrulaması yapar.
- **comment:** `/oc` veya `/opencode` ile tetiklenir; yorumlara yanıt verir.

## Lisans

GPLv3
