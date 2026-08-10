PYTHON ?= python3

.PHONY: test verify clean

test: verify

verify:
	$(PYTHON) tests/verify.py

clean:
	rm -rf .coverage __pycache__ tests/__pycache__