.PHONY: check test maturity clean

# Tek komutla tüm doğrulamalar
check: test maturity

test:
	python3 -m unittest discover -s tests -q

maturity:
	python3 scripts/check_maturity.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +