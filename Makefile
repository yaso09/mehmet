PYTHON ?= python3

.PHONY: validate test maturity all

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v

maturity:
	$(PYTHON) scripts/maturity.py

all: validate test maturity
