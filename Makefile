.PHONY: check score test all

check:
	python3 scripts/healthcheck.py

score:
	python3 scripts/maturity.py

test: check score

all: test