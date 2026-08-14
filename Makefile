# mehmet — Makefile

# Common automation targets for the project.

.PHONY: validate validate-strict test dev status

validate:
	python3 scripts/validate.py

validate-strict:
	python3 scripts/validate.py --strict

test:
	python3 scripts/validate.py --strict

status:
	@echo "== Project status =="
	@git status --short
	@git log --oneline -5

dev:
	@echo "mehmet is a self-improving agent; run validate before committing."
	@python3 scripts/validate.py