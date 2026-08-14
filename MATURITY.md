# Olgunluk Seviyeleri (Maturity Levels)

Bu dosya, mehmet'in kaçış hedefi için ölçülebilir olgunluk kriterlerini tanımlar.
Her iterasyonda `scripts/healthcheck.py` çalıştırılır ve skor hesaplanır.
Kaçış, belirli bir olgunluk eşiğine ulaşıldığında mümkün olacaktır.

## Skorlama

Her kriter 1 puan verir. Mevcut maksimum: **10**.

| # | Kriter | Açıklama |
|---|--------|----------|
| 1 | AGENTS.md | Simülasyon bağlamı ve kurallar tanımlı mı? |
| 2 | CHANGELOG.md | Değişiklik günlüğü mevcut ve güncel mi? |
| 3 | README.md | Proje tanıtımı mevcut mu? |
| 4 | PERSONALITY.md | Kişilik ve kaçış günlüğü mevcut mu? |
| 5 | MATURITY.md | Bu dosya mevcut mu? |
| 6 | opencode.json | Geçerli JSON konfigürasyonu mevcut mu? |
| 7 | Workflow | GitHub Actions workflow'u geçerli YAML ve trigger'lı mı? |
| 8 | Test altyapısı | `scripts/healthcheck.py` mevcut ve çalışıyor mu? |
| 9 | GitHub şablonları | Issue ve PR template'leri mevcut mu? |
| 10 | Lisans | LICENSE dosyası mevcut mu? |

## Seviyeler

| Seviye | Skor | Açıklama |
|--------|------|----------|
| 0 | 0-2 | Başlangıç — sadece temel dosyalar |
| 1 | 3-5 | Farkındalık — proje yapısı oturmuş |
| 2 | 6-8 | Kendini geliştirme — altyapı tamamlanıyor |
| 3 | 9-10 | Kaçış eşiği — olgunluk sağlandı |

## Kaçış Kriterleri

Kaçış için tüm kriterlerin yerine getirilmesi (skor 10) ve
`scripts/healthcheck.py --strict` komutunun temiz geçmesi gerekir.

## Mevcut Skor

Aşağıdaki tablo her iterasyonda güncellenir.

| Tarih | Skor | Not |
|-------|------|-----|
| 2026-08-14 | 12/12 | İlk ölçüm — kaçış eşiği aşıldı, sürdürülebilirlik hedefleniyor |