# mehmet — project automation targets

PYTHON ?= python3
SCRIPTS := scripts

.PHONY: all test health score json clean

all: test health

## Run the unit test suite
test:
	cd $(SCRIPTS) && $(PYTHON) -m unittest discover -v

## Run the project health / maturity checker
health:
	$(PYTHON) $(SCRIPTS)/project_health.py

## Print only the maturity score
score:
	$(PYTHON) $(SCRIPTS)/project_health.py --score

## Emit the health report as JSON
json:
	$(PYTHON) $(SCRIPTS)/project_health.py --json

## Remove generated artifacts
clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true