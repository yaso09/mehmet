.PHONY: test maturity report check clean

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v

maturity:
	python3 scripts/maturity.py

report:
	python3 scripts/maturity.py > docs/maturity-report.md
	@echo "Report written to docs/maturity-report.md"

check: test maturity

clean:
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -f .coverage 2>/dev/null || true
	@echo "Cleaned."