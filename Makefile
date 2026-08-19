.PHONY: test maturity check

test:
	python3 -m pytest -q

maturity:
	python3 scripts/maturity.py

check: test maturity
