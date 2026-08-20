VERSION := $(shell cat VERSION 2>/dev/null || echo 0.0.0)
PYTHON ?= python3

.PHONY: check test health report all

## check: run all validation (tests + health gate)
check: test health

## test: run the unit test suite
test:
	$(PYTHON) -m unittest discover -s scripts/tests -v

## health: compute maturity score and enforce escape threshold
health:
	$(PYTHON) scripts/mehmet_health.py --root . --report docs/health-report.md

## report: regenerate docs/health-report.md without failing on low score
report:
	$(PYTHON) scripts/mehmet_health.py --root . --report docs/health-report.md || true

## all: verify the full project like CI does
all: check
