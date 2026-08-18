.PHONY: validate help all

help:
	@echo "mehmet development commands"
	@echo "  make validate   - run project health validation"
	@echo "  make all        - validate then summary"

validate:
	python3 scripts/validate.py

all: validate
	@echo "Project is healthy."