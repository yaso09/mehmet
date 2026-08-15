.PHONY: validate maturity check test

validate:
	@bash tests/validate.sh

maturity:
	@bash scripts/maturity.sh

check: validate maturity

test: validate