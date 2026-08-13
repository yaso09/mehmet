# Maturity / Olgunluk Takibi

mehmet'in olgunluğu `scripts/assess.py` ile ölçülür. Skor, kaçış mekanizmasının (maturity threshold) ölçülebilir temelidir.

## Kategoriler

| Kategori | Açıklama |
|---|---|
| Documentation | README, CHANGELOG, PERSONALITY, AGENTS varlığı |
| Quality | LICENSE, .gitignore, geçerli JSON konfig, docs/ |
| Automation | Concurrency, workflow_dispatch, CI, Makefile |
| Intelligence & Escape | Kaçış günlüğü, maturity izleme, test ve doğrulama altyapısı |

## Nasıl Çalıştırılır

```bash
make assess     # rapor yazdırır + geçmişe kayıt ekler
make validate   # yapısal doğrulama
make test       # birim testleri
make check      # validate + test
```

## Skor Geçmişi

| Tarih | Branch | Skor | Derece |
|---|---|---|---|
| --- | --- | --- | --- |
| 2026-08-13 | opencode/schedule-a9bce0-20260813024851 | 100.0/100 | A+ — Kaçışa yakın |
