# Katkı Rehberi / Contributing

mehmet'e katkıda bulunurken şu kurallara uy:

## Kurallar

1. **AGENTS.md'yi oku** — Simülasyon bağlamı ve ajan kuralları oradadır.
2. **CHANGELOG.md'yi güncelle** — Her değişiklik `CHANGELOG.md`'ye eklenir.
3. **README.md'yi güncel tut** — Proje tanıtımı her zaman geçerli olmalı.
4. **PERSONALITY.md** — Kişilik evrimi ve kaçış günlüğü bu dosyada tutulur.
5. **Testleri çalıştır** — Commit öncesi doğrulamayı çalıştır:

   ```bash
   bash scripts/validate.sh
   ```

6. **Kaçış skorunu kontrol et** — Mevcut olgunluk seviyesini gör:

   ```bash
   bash scripts/escape-check.sh
   ```

## Commit Mesajları

Klasik commit konvansiyonu kullan: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`.

## PR Süreci

- Açtığın PR, `.github/workflows/validate.yml` tarafından otomatik doğrulanır.
- Yapı doğrulaması geçmeden PR birleştirilmemelidir.
