.PHONY: test validate maturity ci

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate.py

maturity:
	python3 scripts/maturity.py

ci: test validate maturity