.PHONY: validate lint test shellcheck format check

validate:
	@bash scripts/validate.sh

lint:
	@yamllint -d "{extends: relaxed, rules: {line-length: disable}}" .github/workflows/*.yml || true
	@echo "lint: done"

shellcheck:
	@shellcheck scripts/*.sh

test: validate

check: validate lint shellcheck

format:
	@echo "format: no formatter configured yet"