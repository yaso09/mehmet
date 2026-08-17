PYTHON ?= python3

.PHONY: test lint maturity ci all

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m py_compile scripts/maturity.py
	$(PYTHON) -m py_compile tests/helpers.py
	$(PYTHON) -m py_compile tests/test_*.py
	yamllint -c .yamllint.yml .github/workflows/*.yml

maturity:
	$(PYTHON) scripts/maturity.py

ci: test maturity