.PHONY: check test help

PYTHON ?= python3

check: ## Run the project self-check
	$(PYTHON) scripts/self_check.py

test: ## Run the unit test suite
	$(PYTHON) -m unittest discover -s tests -v

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'
