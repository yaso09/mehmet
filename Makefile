PYTHON := python3

.PHONY: test validate maturity docs clean

## Run the project test suite
test:
	$(PYTHON) -m unittest discover -s tests -v

## Run project tests and compute maturity score
validate: test
	$(PYTHON) scripts/maturity.py

## Compute and append the maturity / escape score
maturity:
	$(PYTHON) scripts/maturity.py

## Show available make targets
docs:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

## Remove Python bytecode caches
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true