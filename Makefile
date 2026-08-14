# mehmet - Makefile
# Ortak görevler için kısayollar.

SHELL := /usr/bin/env bash
.PHONY: validate test maturity check ci clean

## validate: Proje bütünlüğünü doğrula
validate:
	bash scripts/validate.sh

## test: Test suite'ini çalıştır
test:
	bash tests/test_validate.sh

## maturity: Olgunluk skorunu raporla
maturity:
	python3 scripts/maturity.py

## check: validate + test
check: validate test

## ci: check + maturity (CI için)
ci: check maturity

## clean: Geçici dosyaları temizle
clean:
	rm -rf .firecrawl/ __pycache__/ .pytest_cache/
	find . -name '*.pyc' -delete 2>/dev/null || true