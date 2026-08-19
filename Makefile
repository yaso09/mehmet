.PHONY: all validate test lint

all: validate test

validate:
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -v

lint:
	python3 -m py_compile scripts/validate.py tests/test_validate.py
