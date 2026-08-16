.PHONY: verify maturity check ci help

help:
	@echo "mehmet make targets:"
	@echo "  make verify   - run project health verification"
	@echo "  make maturity - compute maturity score"
	@echo "  make check    - verify + maturity"

verify:
	python3 scripts/verify.py

maturity:
	python3 scripts/maturity.py

check: verify maturity
	@echo "All checks passed."