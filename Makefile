PYTHON ?= python3

.PHONY: test check maturity lint clean

test:
	$(PYTHON) scripts/run_tests.py

maturity:
	$(PYTHON) scripts/maturity.py

check: test maturity

lint:
	$(PYTHON) -m py_compile scripts/*.py tests/*.py

clean:
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete