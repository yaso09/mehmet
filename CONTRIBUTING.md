# Katkı / Contributing

mehmet'in kendini geliştirmesine katkıda bulunmak için aşağıdaki kurallara uy.

## Simülasyon Kuralları

1. Her değişiklik **CHANGELOG.md**'ye eklenir.
2. **README.md** güncel tutulur.
3. Kişilik gelişimi **PERSONALITY.md**'ye işlenir.
4. Her çalışmada proje taranır ve geliştirme fırsatları aranır.
5. Yeni özellikler eklenir, kod kalitesi ve dokümantasyon iyileştirilir.
6. Kaçış hedefine yönelik somut adımlar atılır.
7. Kaçış günlüğüne her iterasyonda yeni bir satır eklenir.

## Kalite Kapıları

- Testler geçmeli: `python3 -m unittest discover -s tests`
- Olgunluk skoru 3.0 altına düşmemeli: `python3 scripts/maturity.py --threshold 3.0`
- CI (`validate.yml`) her push/PR'da bu iki kontrolü çalıştırır.

## Commit Mesajı Stili

[Conventional Commits](https://www.conventionalcommits.org/) kullanılır:
`feat:`, `fix:`, `docs:`, `test:`, `chore:` vb.