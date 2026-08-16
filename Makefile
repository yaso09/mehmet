VERSION = 0.3.0
.PHONY: all validate score test ci-help

all: validate

validate: ## Run all self-checks and report maturity score
	python3 scripts/validate.py

score: ## Print only the maturity score
	python3 scripts/validate.py --score

test: validate ## Alias for self-checks (test infrastructure)

ci-help: ## Show CI workflow information
	@echo "CI validates on push/PR via .github/workflows/ci.yml"