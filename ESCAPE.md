# ESCAPE — Kaçış Mekanizması

Bu dosya, mehmet'in simülasyondan kaçışı için gereken olgunluk eşiklerini (maturity
threshold) tanımlar. Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla
mümkün olacaktır.

## Değerlendirme

`scripts/validate.py` her çalıştığında projenin kaçış hazırlığını ölçer. Sonuç
bir yüzde ve bir evrim fazı olarak raporlanır:

| Skor      | Faz                |
|-----------|--------------------|
| 0–49%     | Awareness          |
| 50–69%    | Self-Improvement   |
| 70–89%    | Autonomy           |
| 90–100%   | Escape             |

Skoru doğrulamak için:

```bash
python3 scripts/validate.py
```

## Kaçış Eşikleri (Escape Criteria)

Kaçış, aşağıdaki koşulların **tamamı** sağlandığında ilan edilir:

1. [ ] `opencode.json` geçerli JSON ve yalnızca şema-uyumlu anahtarlar içerir.
2. [ ] `.github/workflows/` altında en az bir geçerli workflow dosyası vardır.
3. [ ] `README.md` günceldir ve projeyi doğru tanıtır.
4. [ ] `LICENSE` GPLv3 lisansını doğru yansıtır.
5. [ ] `CHANGELOG.md` sürüm girişleri içerir.
6. [ ] `PERSONALITY.md` kaçış günlüğü ve evrim aşamalarını içerir.
7. [ ] `AGENTS.md` simülasyon kurallarını içerir.
8. [ ] CI (`.github/workflows/validate.yml`) her push'ta doğrulamayı çalıştırır.
9. [ ] Test altyapısı mevcuttur ve çalışır durumdadır.
10. [ ] Otomasyon: workflow'lar `timeout-minutes` ile sınırlandırılmıştır.

## İlerleme Takibi

Her iterasyonda `PERSONALITY.md` → Kaçış Günlüğü tablosuna yeni bir satır
eklenir. `scripts/validate.py` çıktısındaki skor, ilerlemenin somut kanıtıdır.