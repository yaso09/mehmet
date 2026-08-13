.PHONY: help test validate maturity all

help:
	@echo "Targets:"
	@echo "  test       Run project health tests"
	@echo "  validate   Validate YAML workflow files"
	@echo "  maturity   Compute and log maturity score"
	@echo "  all        Run test + validate + maturity"

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]; print('All YAML valid')"

maturity:
	python3 scripts/maturity.py

all: test validate maturity
