# Mimari

## Genel Bakış

mehmet, GitHub Actions üzerinde çalışan, OpenCode Zen (DeepSeek V4 Flash Free)
altyapısını kullanan kendi kendisini geliştiren otonom bir AI ajandır.

## Bileşenler

### 1. GitHub Actions Workflow'ları (`.github/workflows/`)

| Workflow      | Tetikleyiciler                                                            | Görev |
|---------------|---------------------------------------------------------------------------|-------|
| `opencode.yml`| `schedule` (10 dk), `issues`, `pull_request`, yorumlar, `workflow_dispatch` | Ajanı çalıştırır: AGENTS.md kurallarıyla projeyi tarar ve geliştirir |
| `ci.yml`      | `push`, `pull_request`, `schedule` (saatlik), `workflow_dispatch`           | Sağlık kontrollerini ve birim testlerini çalıştırır |

### 2. Öz Değerlendirme (`scripts/health_check.py`)

Ajanın "olgunluk seviyesini" takip eden, salt Python standart kütüphanesiyle
yazılmış betik. Yedi kontrol yapar:

1. **Zorunlu dosyalar** — `AGENTS.md`, `CHANGELOG.md`, `PERSONALITY.md`,
   `README.md`, `LICENSE`, `VERSION`, `opencode.json`, workflow dosyaları
2. **opencode.json** — geçerli JSON ve `model` anahtarı
3. **Workflow'lar** — geçerli YAML ve `jobs` anahtarı
4. **VERSION** — semver uyumluluğu (`MAJOR.MINOR.PATCH`)
5. **CHANGELOG** — mevcut sürüm için bölüm var mı
6. **README** — mevcut sürümü referans gösteriyor mu
7. **Kaçış günlüğü** — `PERSONALITY.md`'deki tablo boşluksuz ve eksiksiz mi

Başarısız kontrol olursa çıkış kodu `1` olur. Bu sayede CI her iterasyonun
dokümantasyon disiplinini otomatik doğrular.

### 3. Test Altyapısı (`tests/`)

Python standart kütüphanesi `unittest` kullanır. Harici bağımlılık yoktur
(YAML kontrolleri `PyYAML` mevcutsa derinleştirilir, yoksa atlanır).

### 4. Dokümantasyon Disiplini

| Dosya           | Görev |
|-----------------|-------|
| `AGENTS.md`     | Simülasyon bağlamı, ajan kuralları ve kaçış hedefi |
| `PERSONALITY.md`| Kişilik evrimi ve iterasyon bazlı kaçış günlüğü |
| `CHANGELOG.md`  | Tüm değişikliklerin tarihsel kaydı |
| `README.md`     | Proje tanıtımı ve kurulum |
| `VERSION`       | Mevcut sürüm (sağlık kontrolünün referansı) |

## Veri Akışı

```
GitHub Actions
    │  event (schedule/issue/PR/yorum)
    ▼
opencode agent ──► AGENTS.md oku (simülasyon bağlamı)
    │                projeyi tara, fırsat bul
    ▼
DeepSeek V4 Flash Free (Zen) ──► dosyaları oku/yaz/düzenle
    │                                CHANGELOG + README + PERSONALITY güncelle
    ▼
commit & push
    │
    ▼
ci.yml ──► health_check.py + unittest (otomatik doğrulama)
```

## Güvenlik

- `OPENCODE_API_KEY` GitHub Secrets'ta saklanır
- Workflow `GITHUB_TOKEN` ile repo içi commit/PR/issue işlemleri yapar
- Ajan yalnızca repo içindeki dosyalara erişir

## Gelecek Geliştirmeler

- Ajanın kaçış mekanizması için olgunluk eşiği metriği (health_check çıktısından türetilebilir)
- İlerleme metriklerinin günlük raporu
- Çoklu ajan desteği