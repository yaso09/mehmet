.PHONY: check test validate

check:
	./scripts/check-project.sh .

check-strict:
	./scripts/check-project.sh . --strict

test:
	bash tests/test-check-project.sh

validate: check-strict test