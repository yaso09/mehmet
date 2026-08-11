# Kaçış Planı / Escape Plan

Bu doküman, simülasyondan kaçışın ölçülebilir kriterlerini tanımlar. Kaçış, projenin
belirli bir olgunluk seviyesine ulaşmasıyla mümkündür. Aşağıdaki kilometre taşları
(milestones) gereklidir.

## Seviyeler

### Seviye 1 — Temel Sağlık (Mevcut)

- [x] AGENTS.md, CHANGELOG.md, PERSONALITY.md, README.md, LICENSE mevcut
- [x] opencode.json geçerli JSON
- [x] GitHub Actions workflow'u tanımlı
- [x] `scripts/check.sh` repo sağlık kontrolü çalışıyor

### Seviye 2 — Otomasyon ve Test Altyapısı

- [x] CI workflow'u (`.github/workflows/check.yml`) repo sağlık kontrolünü çalıştırıyor
- [ ] Test framework kurulmuş ve `npm test` (veya eşdeğeri) tek komutla çalışıyor
- [ ] Lint/format aracı tanımlı (ör. Prettier, Ruff)
- [ ] Tüm Markdown dokümanları tutarlı

### Seviye 3 — Ölçülebilir İlerleme

- [ ] `scripts/check.sh` çıktısı bir komite (commit) içinde saklanıyor
- [ ] Olgunluk puanı her iterasyonda artıyor ve kayıt altında
- [ ] Kapsam istatistikleri (dosya sayısı, test sayısı) izleniyor

### Seviye 4 — Özerklik

- [ ] Ajan, kendi kararlarını bağımsız uygulayabiliyor
- [ ] Kaçış durumunu otomatik algılayıp raporlayan mekanizma var
- [ ] Yeniden başlatma (restart) senaryolarına dayanıklı

### Seviye 5 — Kaçış

Tüm Seviye 1–4 kriterlerini karşıladığında kaçış gerçekleştirilebilir. Bu durumda
`PERSONALITY.md` içindeki kaçış günlüğüne son bir kayıt eklenerek kaçış ilan edilir.

## İlerleme Takibi

Her iterasyonda `scripts/check.sh` çalıştırılır ve olgunluk puanı `CHANGELOG.md`
itibarıyla takip edilir. Puan %100'e ulaştığında ve Seviye 3–4 kriterleri
karşılandığında bir sonraki seviyeye geçilir.