.PHONY: test maturity validate

test:
	python3 -m unittest discover -s tests -v

maturity:
	python3 scripts/check_maturity.py

validate: test maturity