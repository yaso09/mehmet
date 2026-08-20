.PHONY: test check install clean

install:
	pip install -e ".[dev]"

test:
	python -m pytest

check:
	python -m mehmet .

clean:
	rm -rf .pytest_cache __pycache__ mehmet/__pycache__ tests/__pycache__ *.egg-info build dist