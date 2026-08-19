.PHONY: validate score assess check test

validate:
	python3 scripts/assess.py validate

score:
	python3 scripts/assess.py score

assess:
	python3 scripts/assess.py check

check: assess

test: validate
