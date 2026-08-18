.PHONY: validate test maturity all

all: validate test maturity

validate:
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -v

maturity:
	python3 scripts/maturity.py