.PHONY: test maturity gate

test:
	python3 -m unittest discover -q

maturity:
	python3 scripts/maturity.py

gate:
	python3 scripts/maturity.py --gate