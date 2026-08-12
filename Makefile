.PHONY: validate test maturity escape all

validate:
	python3 scripts/check.py

test:
	python3 -m unittest discover -s scripts/tests

maturity:
	python3 scripts/maturity.py

escape: maturity

all: validate test maturity