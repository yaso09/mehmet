.PHONY: validate maturity status test all

all: validate maturity

validate:
	python3 scripts/validate.py

maturity:
	python3 scripts/maturity.py

status:
	@echo "Maturity score:"
	@python3 scripts/maturity.py
	@echo
	@echo "Validation:"
	@python3 scripts/validate.py

test:
	python3 -m unittest discover -s scripts -p "test_*.py"

lint:
	yamllint .github/workflows/*.yml