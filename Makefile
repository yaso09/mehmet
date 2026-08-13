.PHONY: assess validate test check

assess:
	python3 scripts/assess.py --record

validate:
	bash scripts/validate.sh

test:
	python3 -m unittest discover -s scripts -p 'test_*.py'

check: validate test
	@echo "check: tüm kontroller geçti"
