.PHONY: test maturity check

# Run the full validation suite
test:
	python3 -m unittest discover -s tests -v

# Compute the escape/maturity score
maturity:
	python3 scripts/maturity.py

# Run everything
check: test maturity