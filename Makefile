.PHONY: help validate test lint

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

validate: ## Run project health checks
	bash scripts/validate.sh

test: validate ## Alias for validate (test infrastructure)

lint: ## Lint shell scripts with shellcheck
	shellcheck scripts/*.sh
