.PHONY: help check maturity

help:
	@echo "mehmet — self-improving autonomous agent"
	@echo ""
	@echo "targets:"
	@echo "  check     validate repository structure (exit 1 on failure)"
	@echo "  maturity  compute escape progress score"
	@echo "  help      show this help"

check:
	bash scripts/check-repo.sh

maturity:
	bash scripts/maturity.sh