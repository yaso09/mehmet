.PHONY: test validate maturity check all

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) scripts/validate.py

maturity:
	$(PYTHON) scripts/maturity.py --write

check: validate test
	@echo "All checks passed."

all: check maturity
