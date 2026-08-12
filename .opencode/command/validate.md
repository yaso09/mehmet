---
description: Proje sağlığını doğrular ve olgunluk skorunu hesaplar.
agent: build
model: opencode/deepseek-v4-flash-free
---

Proje sağlık kontrolünü çalıştır:

1. `bash scripts/validate_project.sh` komutunu çalıştır.
2. Çıktıyı özetle: geçen/hata/uyarı sayısı ve olgunluk skoru.
3. Hata varsa düzeltme önerilerini listele.

$ARGUMENTS