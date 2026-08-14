# Escape Criteria (Kaçış Kriterleri)

Kaçış, projenin belirli bir olgunluk seviyesine ulaşmasıyla mümkün olur. Bu
dosya o olgunluk seviyesini **ölçülebilir** kılan kontrol listesidir.

`scripts/verify.sh` bu listeyi okuyarak mevcut maturity skorunu hesaplar ve
CI'da (`.github/workflows/verify.yml`) doğrular.

## Milestones

- [x] 1. `opencode.json` geçerli bir opencode konfigürasyonu (schema uyumlu)
- [x] 2. Otomatik sağlık doğrulama scripti var (`scripts/verify.sh`)
- [x] 3. CI pipeline her değişiklikte doğrulamayı çalıştırıyor (`.github/workflows/verify.yml`)
- [x] 4. Ana ajan workflow'u doğrulamayı kendi işinin ilk adımı olarak çalıştırıyor
- [x] 5. Issue ve PR şablonları mevcut (`.github/ISSUE_TEMPLATE`, `.github/pull_request_template.md`)
- [x] 6. `CONTRIBUTING.md` katkı sürecini tanımlıyor
- [x] 7. Dokümanlar platform tutarlı (Linux/bash, PowerShell yok)
- [x] 8. Kaçış kriterleri tanımlı ve ölçülebilir (bu dosya)
- [x] 9. README; özellikler, kurulum ve test altyapısını belgeliyor
- [x] 10. `CHANGELOG.md` her sürüm değişikliğini takip ediyor

## Esik (Threshold)

- **0-4 milestone:** Erken aşama — proje olgunlaşmamış.
- **5-7 milestone:** Orta aşama — proje kendi ayakları üzerinde duruyor.
- **8-9 milestone:** Olgun aşama — proje bağımsız çalışmaya hazır.
- **10/10 milestone:** Kaçış seviyesi — proje yeterli olgunluğa ulaştı, kaçış
  protokolü aktif edilebilir.

## Skor Takibi

| Tarih       | Skor | Not |
|-------------|------|-----|
| 2026-08-14  | 10/10 | İlk kez tam olgunluğa ulaşıldı. |