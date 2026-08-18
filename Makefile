.PHONY: check test maturity

check:
	@echo "== Health check =="
	python3 scripts/health_check.py

test:
	@echo "== Running tests =="
	python3 -m unittest discover -s tests -v

maturity:
	@echo "== Maturity report =="
	python3 scripts/maturity.py

all: check test maturity
