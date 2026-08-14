# Katkı Rehberi

mehmet, kendisini geliştiren otonom bir ajandır. Katkılar hem insanlar hem de ajanın kendisi tarafından yapılabilir.

## Süreç

1. **Projeyi tara:** Mevcut durumu `docs/escape-roadmap.md` ve `CHANGELOG.md` üzerinden anla.
2. **Değişiklik yap:** Kod, config veya dokümantasyon geliştir.
3. **Doğrula:** `./scripts/validate.sh` çalıştır — tüm kontroller geçmeli.
4. **Maturity'i güncelle:** Puanlar değiştiyse `docs/maturity.json` ve `docs/escape-roadmap.md`'yi güncelle, `./scripts/maturity.sh` ile doğrula.
5. **Kayıt altına al:** Tüm değişiklikleri `CHANGELOG.md`'ye ekle.
6. **Dokümante et:** Gerekirse `README.md`, `docs/` altındaki belgeleri güncelle.

## Kurallar

- `AGENTS.md` simülasyon kurallarına uy.
- `PERSONALITY.md`'deki kaçış günlüğüne her iterasyonda yeni bir satır ekle.
- Lisans: GPLv3. GPLv3 uyumlu katkılar kabul edilir.
- Gizli bilgi içeren commit yapma (`.env`, API key vb. — `.gitignore` kontrol et).

## Kontrol Listesi

- [ ] `./scripts/validate.sh` geçiyor
- [ ] `CHANGELOG.md` güncellendi
- [ ] `docs/maturity.json` puanları güncel (değiştiyse)
- [ ] Kaçış günlüğü iterasyon eklendi
