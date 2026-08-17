.PHONY: validate maturity check

validate:
	bash scripts/validate.sh

maturity:
	bash scripts/check-maturity.sh

check: validate maturity