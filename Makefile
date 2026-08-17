.PHONY: test validate maturity help

help:
	@echo "test      — test suite'u çalıştır (unittest)"
	@echo "validate  — repo doğrulamalarını çalıştır (changelog, kaçış günlüğü)"
	@echo "maturity  — olgunluk/kaçış skorunu göster"

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate.py

maturity:
	python3 scripts/maturity.py

maturity-json:
	python3 scripts/maturity.py --json
