# Maturity / Kaçış Mekanizması

Kaçış, projenin aşağıda tanımlanan olgunluk eşiğine ulaşmasıyla mümkün olur.
Olgunluk `scripts/check.sh` ile ölçülür (0-100 puan).

## Boyutlar

| Boyut | Açıklama |
|---|---|
| Dokümantasyon | README, CHANGELOG, PERSONALITY, AGENTS, MATURITY, docs |
| Yapılandırma | opencode.json, .gitignore |
| Otomasyon | Ana workflow, doğrulama workflow'u, kontrol scripti |
| Güvenlik | Sırların repo içinde düz metin saklanmaması |

## Ölçüm

Her iterasyonda `scripts/check.sh` çalıştırılır:

- Skor **>= 80** → **OLGUN** — kaçış eşiği karşılandı (exit 0)
- Skor **< 80** → **GELİŞMEKTE** — proje iterasyona devam eder (exit 1)

## Kaçış Kriterleri

1. README.md, CHANGELOG.md, PERSONALITY.md güncel ve geçerli
2. opencode.json geçerli JSON ve model tanımı içeriyor
3. Otomasyon: ana workflow + doğrulama workflow'u + çalıştırılabilir kontrol scripti
4. Sırlar repo içinde düz metin saklanmaz

## Durum

- [ ] Olgunluk eşiği karşılandı (`scripts/check.sh` exit 0)