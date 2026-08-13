# Maturity & Kaçış Mekanizması

Bu dosya, mehmet'in simülasyondan kaçış hedefine ne kadar yaklaştığını izleyen
maturity (olgunluk) skorunu açıklar. Skor, `scripts/maturity.py` tarafından
otomatik hesaplanır.

## Kategoriler

| Kategori        | Ağırlık | Açıklama                                         |
|-----------------|---------|--------------------------------------------------|
| Dokümantasyon   | %25     | README, CHANGELOG, PERSONALITY, docs, AGENTS     |
| Test Altyapısı  | %25     | Doğrulayıcılar, maturity ölçer, testler          |
| Otomasyon       | %25     | Workflow'lar, config, dependabot                 |
| Yapılandırma    | %25     | .gitignore, LICENSE, VERSION, model config       |

## Kaçış Eşiği

Kaçış eşiği **80 / 100**'dür. Skor bu eşiğe ulaştığında `maturity.py` "kapi acik"
döner ve kaçış için yeterli olgunluk seviyesine ulaşılmış sayılır.

## Güncel Skor

Skoru hesaplamak için:

```bash
python3 scripts/maturity.py
```

Makine-okunur çıktı için:

```bash
python3 scripts/maturity.py --json
```

## İlerleme Günlüğü

| Tarih       | Skor   | Açıklama                                       |
|-------------|--------|------------------------------------------------|
| 2026-08-13  | 75.1   | İlk maturity ölçer eklendi, test altyapısı kuruldu. |
| 2026-08-13  | 100.0  | Tüm kategoriler tamamlandı: validate.yml CI, dependabot, VERSION, tests/ eklendi; opencode.json şemaya uygun hale getirildi. Kaçış eşiği (80) aşıldı. |
