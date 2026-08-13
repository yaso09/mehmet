PY := python3

.PHONY: test validate metrics check clean

test:
	$(PY) -m unittest discover -s tests -v

validate: test
	$(PY) -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]"
	@echo "Workflow syntax OK"

metrics:
	$(PY) scripts/maturity.py

check:
	$(PY) scripts/maturity.py --check

clean:
	rm -f METRICS.md
	rm -rf __pycache__ tests/__pycache__
