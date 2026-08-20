PY ?= python3

.PHONY: validate maturity test help

help:
	@echo "Kullanılabilir hedefler:"
	@echo "  make validate   - Proje yapısını doğrula"
	@echo "  make maturity   - Olgunluk skorunu raporla"
	@echo "  make test       - Birim testleri çalıştır"

validate:
	$(PY) scripts/validate.py

maturity:
	$(PY) scripts/maturity.py

test:
	$(PY) -m unittest discover -s tests -v
