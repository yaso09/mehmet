.PHONY: test lint ci help

help:
	@echo "Targets:"
	@echo "  test   Run the project integrity test suite"
	@echo "  lint   Validate config and workflow files"
	@echo "  ci     Full CI pipeline (lint + test)"

test:
	python3 -m unittest discover -s tests -v

lint:
	python3 tests/test_project.py

ci: lint test