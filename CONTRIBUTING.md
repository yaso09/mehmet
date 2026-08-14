# Katkı Rehberi

mehmet, kendini geliştiren otonom bir AI ajandır. Katkılarınız değerlidir.

## Geliştirme Döngüsü

1. Repoyu fork'layın ve klonlayın.
2. Yeni bir dal açın: `git checkout -b feature/ozellik-adi`
3. Değişikliklerinizi yapın.
4. **Zorunlu adımlar:**
   - `python3 -m unittest discover -s tests -v` ile testlerin geçtiğini doğrulayın.
   - `python3 scripts/check_project.py` ile olgunluk kontrolünün PASS döndüğünü doğrulayın.
5. Yaptığınız her değişikliği `CHANGELOG.md`'ye ekleyin.
6. PR açın ve değişiklikleri özetleyin.

## Dosya Yapısı

| Dosya | Açıklama |
|---|---|
| `AGENTS.md` | Simülasyon bağlamı ve kurallar |
| `README.md` | Proje tanıtımı |
| `CHANGELOG.md` | Değişiklik günlüğü |
| `PERSONALITY.md` | Ajan kişiliği ve kaçış günlüğü |
| `opencode.json` | OpenCode konfigürasyonu |
| `scripts/check_project.py` | Olgunluk ve sağlık kontrolü |
| `tests/test_project.py` | Proje testleri |
| `.github/workflows/` | CI/otomasyon workflow'ları |

## Kaçış Kriterleri

Proje, `scripts/check_project.py` üzerinden ölçülen bir olgunluk puanına sahiptir.
Kaçış eşiği 80/100'dür. Yeni özellikler bu puana olumlu katkı sağlamalıdır.
