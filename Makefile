.PHONY: validate test

validate: test

test:
	@python3 tests/test_project.py
