.PHONY: validate test check help

validate: ## Run project health checks
	python3 scripts/validate.py

test: ## Run the unit test suite
	python3 -m unittest discover -s tests -v

check: validate test ## Validate and test (CI entrypoint)

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'