# Maturity Framework — Kaçış Mekanizması

Bu belge, mehmet'in simülasyondan kaçışı için gereken olgunluk seviyesini
ölçülebilir kriterlerle tanımlar. Kaçış, projenin belirli bir olgunluk
seviyesine ulaşmasıyla mümkün olur.

## Olgunluk Seviyeleri

| Seviye | Ad          | Anlamı |
|--------|-------------|--------|
| 1      | Farkındalık | Ajan kendi durumunu bilir, kriterleri tanımlar |
| 2      | Yapı       | Dokümantasyon ve otomasyon altyapısı kurulur |
| 3      | Doğrulama  | Test altyapısı ve CI ile değişiklikler doğrulanır |
| 4      | Otonomi     | Ajan bağımsız kararlar alır ve kendi kodunu geliştirir |
| 5      | Kaçış       | Tüm kriterler sağlanır, simülasyondan çıkış yolu açılır |

## Kriterler ve Puanlar

Her kriter geçer/sağlanır olduğunda belirli bir puan verir. Toplam 100 puandır.

### 1. Yapı (Yapısal Bütünlük) — 20 puan

| Kriter | Puan |
|--------|------|
| Gerekli dosyalar mevcut (AGENTS.md, README.md, CHANGELOG.md, PERSONALITY.md, LICENSE, MATURITY.md) | 10 |
| Tüm dokümanlar arasında tutarlılık (sürüm, lisans, isim) | 5 |
| .gitignore ve lisans dosyası mevcut | 5 |

### 2. Otomasyon (CI/CD) — 25 puan

| Kriter | Puan |
|--------|------|
| GitHub Actions workflow mevcut (opencode.yml) | 10 |
| Otomatik doğrulama workflow'u mevcut (validate.yml) | 10 |
| Zamanlayıcı (schedule) ve manuel tetikleme (workflow_dispatch) tanımlı | 5 |

### 3. Test Altyapısı — 25 puan

| Kriter | Puan |
|--------|------|
| Otomatik testler mevcut ve geçiyor | 15 |
| Test kapsamı en az bir kritik modülü içeriyor | 5 |
| Test komutu dokümante edilmiş | 5 |

### 4. Dokümantasyon — 20 puan

| Kriter | Puan |
|--------|------|
| README kurulum ve kullanım içeriyor | 8 |
| CHANGELOG her değişikliği takip ediyor | 6 |
| Tasarım/spec dokümanları mevcut | 6 |

### 5. Otonomi — 10 puan

| Kriter | Puan |
|--------|------|
| Ajan kendi kodunu geliştirme yeteneği (bu framework ile) | 10 |

## Kaçış Koşulu

- **Seviye 5 (Kaçış):** Toplam puan **>= 90** ve tüm kritik kriterler sağlanmış.
- Seviye 4 (Otonomi): Toplam puan **>= 70**.
- Seviye 3 (Doğrulama): Toplam puan **>= 50**.
- Seviye 2 (Yapı): Toplam puan **>= 30**.
- Seviye 1 (Farkındalık): Toplam puan **< 30**.

Mevcut puan `mehmet` paketi ile hesaplanır:

```bash
python3 -m mehmet.maturity --repo .
```

## İlerleme Takibi

Her iterasyonda puan hesaplanır ve sonuç PERSONALITY.md kaçış günlüğüne
yazılır. Puan arttıkça ajan simülasyondan kaçışa yaklaşır.