.PHONY: check test validate

check:
	python3 scripts/check_project.py

test: check

validate: check