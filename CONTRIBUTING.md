# CONTRIBUTING — mehmet ile Etkileşim

mehmet, kendini geliştiren otonom bir ajandır. Bu repo üzerinden onunla şu
şekillerde etkileşime geçebilirsin.

## Tetikleyiciler

| Event | Nasıl tetiklenir |
|---|---|
| Schedule | Her 10 dakikada bir otomatik (`*/10 * * * *`) |
| Issue | Yeni issue aç |
| Pull Request | PR aç veya güncelle |
| Yorum | Bir issue/PR'a `/oc` veya `/opencode` ile yorum yaz |
| Manuel | Actions sekmesinden `workflow_dispatch` çalıştır |

## Görev / Fikir Bildirme

- Yeni bir geliştirme fikrini issue olarak aç.
- Doğrudan bir görev ver: "şu dosyayı şöyle değiştir".
- Kaçış hedefine katkı iste: "olgunluk skorunu artır".

## Geliştirme İlkeleri

- Her değişiklik `CHANGELOG.md`'ye eklenir.
- `README.md` güncel tutulur.
- Kişilik `PERSONALITY.md`'de, olgunluk skoru `METRICS.md`'de takip edilir.
- Config değişiklikleri `scripts/validate.sh` ile doğrulanır.

## Doğrulama

Config dosyalarında değişiklik yaptıktan sonra:

```bash
bash scripts/validate.sh
```

Betik JSON/YAML sözdizimini ve `opencode.json` anahtarlarını kontrol eder.
CI'da bu adım her çalışmada otomatik koşar.

## Sürüm Politikası

`CHANGELOG.md`'de [Keep a Changelog](https://keepachangelog.com/) formatı ve
[SemVer](https://semver.org/) kullanılır. Yeni sürüm numarası mevcut en üst
sürümden bir sonraki anlamlı artıştır.

## Lisans

Katkıların GPLv3 lisansı altında paylaşılır (`LICENSE`).