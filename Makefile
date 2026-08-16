# mehmet — geliştirme ve doğrulama otomasyonu

PYTHON ?= python3

.PHONY: help test validate maturity install clean

help:
	@echo "Hedefler:"
	@echo "  make install    — paketi editable olarak kur"
	@echo "  make test       — birim testleri çalıştır"
	@echo "  make validate   — testleri çalıştır ve olgunluk skorunu raporla"
	@echo "  make maturity   — olgunluk skorunu raporla"
	@echo "  make clean      — build/cache dosyalarını temizle"

install:
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m unittest discover -s tests -v

maturity:
	$(PYTHON) -m mehmet . || true

validate: test maturity

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true