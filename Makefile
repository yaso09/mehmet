.PHONY: validate test maturity all

validate:
	bash scripts/validate.sh

test:
	bash tests/run_tests.sh

maturity:
	bash scripts/maturity.sh

all: validate test maturity
