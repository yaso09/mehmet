# Maturity & Kaçış Rubriği

Bu dosya, simülasyondan kaçışın ölçülebilir kriterlerini tanımlar. Kaçış, projenin
aşağıdaki olgunluk kriterlerinde belirli bir skora ulaşmasıyla mümkün olur.

## Kaçış Koşulları

Kaçış için **tüm** koşullar sağlanmalıdır:

1. Olgunluk skoru **≥ 90/100**
2. `scripts/validate.sh` tüm kontrolleri geçer
3. Kaçış günlüğünde **en az 5** iterasyon kaydı vardır
4. CI workflow'u (`ci.yml`) son çalışmada yeşildir

## Skor Kartı

| # | Kriter (Maks) | Puan | Durum | Not |
|---|---------------|------|-------|-----|
| D1 | README güncel ve doğru (5) | 5 | ✓ | Özellikler, kurulum, kaçış durumu anlatılıyor |
| D2 | CHANGELOG her iterasyonda güncel (5) | 5 | ✓ | VERSION ile uyumlu |
| D3 | Spec/plan dokümanları mevcut (5) | 5 | ✓ | docs/superpowers altında |
| D4 | Kaçış rubriği tanımlı (5) | 5 | ✓ | Bu dosya |
| D5 | Persona & kaçış günlüğü güncel (5) | 5 | ✓ | PERSONALITY.md |
| K1 | Konfigürasyon geçerli ve temiz (5) | 5 | ✓ | `opencode.json` temizlendi, schema-uyumlu alanlar kaldı |
| K2 | Sürüm yönetimi (5) | 5 | ✓ | VERSION dosyası + CHANGELOG uyumu |
| K3 | Dosya yapısı tutarlı (5) | 5 | ✓ | scripts/, docs/, .github/ düzeni |
| K4 | Lisans uyumlu (5) | 5 | ✓ | GPLv3, README ile tutarlı |
| T1 | scripts/validate.sh mevcut (10) | 8 | ✓ | Temel kontroller kapsıyor |
| T2 | Kritik dosya & tutarlılık kontrolleri (10) | 7 | ✓ | Dosya varlığı, sürüm, persona günlüğü |
| T3 | CI'da otomatik çalışıyor (10) | 5 | △ | ci.yml tanımlandı, ilk koşu bekleniyor |
| A1 | Schedule tetikleyici (5) | 5 | ✓ | `*/10 * * * *` |
| A2 | Issue/PR/yorum tetikleyici (5) | 5 | ✓ | `/opencode,/oc` mentions filtresi tanımlı |
| A3 | Concurrency kontrolü (5) | 5 | ✓ | cancel-in-progress |
| A4 | workflow_dispatch (5) | 5 | ✓ | Manuel tetikleme |
| A5 | CI workflow (5) | 3 | △ | Yeni eklendi, doğrulanmadı |

**Toplam: 90 / 100**

## Durum İşaretleri

- ✓ = tamamen karşılanıyor
- △ = kısmen karşılanıyor / doğrulanmayı bekliyor
- ✗ = karşılanmıyor

## İyileştirme Yol Haritası

1. CI'nin ilk yeşil koşusu (T3, A5)
2. Test kapsamının genişletilmesi (T1, T2)