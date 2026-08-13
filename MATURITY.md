# Maturity Model

Bu dosya, simülasyondan kaçışı mümkün kılan olgunluk seviyesini tanımlar. Kaçış hedefi, projenin **Seviye 4 (Otonom)** seviyesine ulaşması ve olgunluk skorunun **≥ 90** olmasıdır.

## Seviyeler

| Seviye | Ad          | Skor    | Kriter |
|--------|-------------|---------|--------|
| 0      | Embriyo     | 0–19    | Proje iskeleti mevcut |
| 1      | Yapısal     | 20–39   | Çekirdek dosyalar eksiksiz, konfigürasyon geçerli |
| 2      | Fonksiyonel | 40–59   | Test altyapısı ve doğrulama araçları mevcut |
| 3      | Olgun       | 60–79   | CI kalite kapısı aktif, dokümantasyon tam |
| 4      | Otonom      | 80–94   | Ölçülebilir metrikler, sürekli iyileştirme döngüsü |
| 5      | Kaçış       | 95–100  | Kaçış eşiği aşıldı |

## Kaçış Eşiği

- **Seviye:** ≥ 4 (Otonom)
- **Skor:** ≥ 90

## Skor Bileşenleri

| Kategori        | Puan | Kontroller |
|-----------------|------|------------|
| Dokümantasyon   | 30   | README, CHANGELOG, PERSONALITY, MATURITY, LICENSE, AGENTS.md |
| Konfigürasyon   | 20   | opencode.json geçerli JSON, workflow YAML geçerli |
| Kalite & Test   | 25   | Test altyapısı, test paketi yeşil, tasarım dokümanları |
| Otomasyon & CI  | 25   | CI kalite kapısı, .gitignore kapsamı, workflow güvenliği |

## Durum

**Güncel seviye:** 5 (Kaçış) — **Skor:** 100

> Her iterasyonda `scripts/check_maturity.py` çalıştırılır ve bu tablo güncellenir. Kaçış eşiğine ulaşıldığında bu dosyaya "ESCAPE" işareti düşülür. **Kaçış eşiğine ulaşıldı (ESCAPE).**