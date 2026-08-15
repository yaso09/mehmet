.PHONY: test maturity check all

test:
	bash tests/run_tests.sh

maturity:
	bash scripts/maturity.sh

check: test maturity
	@echo "Tüm kontroller geçti."

all: check
	@echo "Proje hazır."