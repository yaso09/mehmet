SHELL := /bin/bash

.PHONY: test report strict clean

test:
	python -m unittest discover -s tests -t . -p 'test_*.py' -v

report:
	python scripts/check_maturity.py

strict:
	python scripts/check_maturity.py --strict

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true