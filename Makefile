PYTHON ?= python3

.PHONY: test maturity verify report

## Run the full test suite
test:
	$(PYTHON) -m unittest discover -s tests -v

## Compute maturity score and regenerate the report
maturity:
	$(PYTHON) scripts/maturity.py

## Run tests and regenerate the maturity report
verify: test maturity

## Regenerate the maturity report only
report:
	$(PYTHON) scripts/maturity.py --report-only