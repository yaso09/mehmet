.PHONY: all test check health lint

all: check

test:
	./scripts/run-tests.sh

check:
	bash -n scripts/*.sh tests/*.sh
	./scripts/run-tests.sh

health:
	./scripts/check-health.sh

lint:
	@if command -v shellcheck >/dev/null 2>&1; then \
		shellcheck scripts/*.sh tests/*.sh; \
	else \
		echo "shellcheck not installed — skipping"; \
	fi