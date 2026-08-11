.PHONY: test check help

help:
	@echo "Available targets:"
	@echo "  test   Run repo health tests (python3 -m unittest)"
	@echo "  check  Alias for test"

test:
	python3 -m unittest discover -s tests -v

check: test
