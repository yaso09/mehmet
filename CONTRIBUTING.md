# Katkı Rehberi

Katkılarınız sayesinde mehmet simülasyondan kaçışa bir adım daha yaklaşır. Bize nasıl yardım edebileceğinizi aşağıda bulabilirsiniz.

## Geliştirme Ortamı

```bash
git clone https://github.com/yaso09/mehmet
cd mehmet
pip install -r requirements.txt
```

## Kalite Kapıları

Değişiklik göndermeden önce aşağıdaki kontrolleri yerel ortamda çalıştırın:

```bash
bash scripts/check_project.sh        # proje yapısı sağlık kontrolü
PYTHONPATH=src python -m unittest discover -s tests -v   # unit testler
ruff check src tests                 # lint
bash scripts/maturity.sh             # olgunluk skoru
```

## Süreç

1. Kendi branch'inizi açın: `git checkout -b feature/iyilestirme`
2. Değişikliklerinizi yapın ve CHANGELOG.md'ye not düşün.
3. Testleri çalıştırın (yukarıdaki kalite kapıları).
4. Pull Request açın. Quality (CI) job'ı otomatik olarak kontrol eder.

## Kurallar

- Her değişiklik CHANGELOG.md'ye eklenmeli.
- README.md güncel tutulmalı.
- Yeni davranışlar için unit test ekleyin.
- Kod stili: `ruff` kuralları (pyproject.toml içinde tanımlı).