# Katkı Rehberi

mehmet'e katkıda bulunduğun için teşekkürler. Bu proje otonom bir AI ajanı tarafından
sürekli geliştirilmektedir; ancak insan katkıları da memnuniyetle karşılanır.

## Geliştirme Akışı

1. Repo'yu fork et ve `main` dalından yeni bir dal aç.
2. Değişikliklerini yap.
3. Yerel doğrulamayı çalıştır:

   ```bash
   make validate
   ```

4. Aşağıdaki kurallara uyduğundan emin ol:
   - Her değişiklik `CHANGELOG.md` içine uygun sürüm başlığı altında eklenmeli.
   - `README.md` güncel kalmalı.
   - Kişilik/bağlam değişiklikleri `PERSONALITY.md` ve `AGENTS.md` içinde yapılmalı.
   - `OPENCODE_API_KEY` gibi secret'lar asla commit'lenmemeli.
5. Değişikliklerini açıkla ve `validate` workflow'unun geçtiğinden emin ol.

## Kod Kalitesi

- Python betikleri sıfır harici bağımlılıkla çalışmalı (yalnızca stdlib).
- Yeni metrik/check eklenirse `scripts/maturity.py` ve `scripts/validate.py`
  senkron tutulmalı.
- Değişiklik öncesi/sonrası olgunluk skorunu karşılaştırmak için:

   ```bash
   make maturity
   ```

## Issue / PR

- Net ve tek amaçlı PR'lar tercih edilir.
- Issue'larda beklenti ve yeniden üretme adımları açık olmalı.
