# Katkıda Bulunma (Contributing)

mehmet kendi kendisini geliştiren bir ajandır, ancak insan katkıları da hoş karşılanır.

## Geliştirme Döngüsü

1. Projeyi klonlayın
2. Değişikliklerinizi yapın
3. `python scripts/health_check.py` ile sağlık kontrollerini çalıştırın
4. `python -m unittest discover -s tests -v` ile testleri çalıştırın
5. Aşağıdaki kurallara uygun şekilde commit atın

## Zorunlu Kurallar

- Her değişiklik `CHANGELOG.md`'ye eklenmelidir
- Yeni sürüm numarası `VERSION` dosyasına yazılmalıdır (semver: `MAJOR.MINOR.PATCH`)
- `README.md` güncel tutulmalı ve mevcut sürümü referans göstermelidir
- `PERSONALITY.md`'deki kaçış günlüğü her iterasyonda bir satır ilerlemelidir
- `AGENTS.md`'deki simülasyon kurallarına uyulmalıdır

## Yapı

```
.
├── AGENTS.md                  # Simülasyon bağlamı ve kurallar
├── CHANGELOG.md               # Değişiklik günlüğü
├── PERSONALITY.md             # Kişilik evrimi ve kaçış günlüğü
├── README.md                  # Proje tanıtımı
├── VERSION                    # Mevcut sürüm numarası
├── opencode.json              # OpenCode konfigürasyonu
├── scripts/
│   └── health_check.py        # Sağlık kontrolü ve öz değerlendirme
├── tests/
│   └── test_health_check.py   # Sağlık kontrolü testleri
├── docs/
│   ├── ARCHITECTURE.md        # Mimari belgesi
│   └── superpowers/           # Tasarım ve plan belgeleri
└── .github/workflows/
    ├── opencode.yml           # Ajan workflow'u
    └── ci.yml                 # CI: sağlık + test
```

## Test Kapsamı

Yeni bir fonksiyon eklerken veya mevcut davranışı değiştirirken
`tests/test_health_check.py` dosyasına karşılık gelen testleri ekleyin.
Tüm testler geçmeden değişiklik commit edilmemelidir.