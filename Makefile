.PHONY: test verify score check install

test:
	python -m pytest

verify:
	python scripts/verify_project.py

score:
	python scripts/escape_score.py

check: test verify

install:
	python -m pip install --upgrade pip pytest