.PHONY: test maturity install

test:
	python -m pytest -q

maturity:
	python -m mehmet .

install:
	pip install -e .
