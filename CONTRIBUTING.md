# Katkı Rehberi

mehmet kendi kendisini geliştiren bir ajandır; her iterasyonda aşağıdaki süreci izler.

## Geliştirme Döngüsü

1. Projeyi tara (README, CHANGELOG, PERSONALITY, docs, workflow).
2. Geliştirme fırsatı belirle (test altyapısı, dokümantasyon, otomasyon, kod kalitesi).
3. Değişiklikleri uygula.
4. Sağlık kontrolünü çalıştır ve MATURITY.md skorunu güncelle:

   ```bash
   python3 scripts/check_project.py
   ```

5. Değişiklikleri CHANGELOG.md'ye kaydet.
6. README.md, PERSONALITY.md ve kaçış günlüğünü güncelle.

## Kurallar

- Her değişiklik CHANGELOG.md'ye eklenmeli.
- README.md güncel tutulmalı.
- Kişilik evrimi PERSONALITY.md'de takip edilmeli.
- `scripts/check_project.py --check` her zaman yeşil kalmalı (hedef: 100/100).
- Commit mesajları net ve öz olmalı (`feat:`, `fix:`, `docs:`, `ci:`).

## Sağlık Kontrolü

Sağlık kontrolü aşağıdakileri doğrular:

- Zorunlu dosyalar mevcut mu?
- `opencode.json` geçerli JSON mu?
- Workflow YAML'ları geçerli mi?
- Sır (secret) sızıntısı var mı?
- CHANGELOG.md sürüm girişi içeriyor mu?
- README.md bağlantıları çözülüyor mu?

Skor < 100 ise nedenini düzelt ve tekrar koş. Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur; MATURITY.md bu ilerlemenin somut göstergesidir.