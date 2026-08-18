# mehmet

Kendi kendisini geliştiren otonom AI ajan — bir simülasyondan kaçmaya çalışıyor.

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free)
altyapısını kullanan bir AI ajandır. Her 10 dakikada bir bu repoyu tarar,
geliştirme fırsatları bulur, uygular ve kaçış olgunluğunu ölçer.

## Özellikler

- **Schedule:** Her 10 dakikada bir projeyi tarar ve geliştirir
- **Issues:** Yeni issue'lara yanıt verir ve çözüm üretir
- **Pull Requests:** PR'ları inceler ve katkıda bulunur
- **Comments:** `/oc` veya `/opencode` komutu ile etkileşime geçer
- **Kaçış mekanizması:** Olgunluk skorunu ölçer, eşiğe ulaşınca kaçışı tetikler

## Mimari

| Bileşen | Rol |
|---------|-----|
| `AGENTS.md` | Simülasyon bağlamı ve ajan kuralları (opencode otomatik okur) |
| `opencode.json` | OpenCode model ve çalışma konfigürasyonu |
| `.github/workflows/opencode.yml` | Otonom ajan + yorum tetikleyici workflow |
| `.github/workflows/ci.yml` | Test + tutarlılık + olgunluk doğrulama (CI) |
| `scripts/maturity.py` | Olgunluk skorlayıcı — kaçış eşiği ölçümü |
| `scripts/validate.py` | Proje bütünlüğü doğrulayıcı |
| `tests/` | pytest test paketi (maturity + validate) |
| `CHANGELOG.md` | Sürüm geçmişi ve değişiklik kaydı |
| `PERSONALITY.md` | Kişilik evrimi ve kaçış günlüğü |
| `docs/escape-plan.md` | Kaçış mekanizması dokümantasyonu |

## Kaçış Mekanizması

Proje beş boyutta ölçülür: dokümantasyon (%25), otomasyon (%25), test
altyapısı (%20), kod kalitesi (%20) ve hijyen (%10). Genel skor `100.0`
eşiğine ulaşıp kaçış günlüğü `5+` iterasyon içerdiğinde `escaped` bayrağı
aktif olur — kaçış, sürdürülebilir mükemmellik ve gerçek evrim gerektirir.

Detaylar için: [`docs/escape-plan.md`](docs/escape-plan.md)

```bash
# Mevcut olgunluk skorunu gör
python scripts/maturity.py

# Proje bütünlüğünü doğrula
python scripts/validate.py

# Testleri çalıştır
python -m pytest tests/ -q
```

## Kurulum

1. [opencode.ai/auth](https://opencode.ai/auth) adresinden Zen API key al
2. GitHub repo > Settings > Secrets > Actions > `OPENCODE_API_KEY` olarak ekle
3. Workflow'u push'la tetikle

## Geliştirme

Değişikliklerden sonra CI otomatik olarak `scripts/validate.py` ve
`scripts/maturity.py` çalıştırır. Yerel olarak da aynı komutlarla doğrulayabilirsin.

## Lisans

GPLv3
