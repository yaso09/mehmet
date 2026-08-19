.PHONY: test check yaml validate help

help:
	@echo "test     - unit testleri çalıştırır"
	@echo "check    - repo sağlık kontrolü yapar"
	@echo "yaml     - workflow YAML dosyalarını doğrular"
	@echo "validate - test + check + yaml"

test:
	python3 -m unittest discover -s tests -v

check:
	python3 scripts/repo_health.py

yaml:
	python3 scripts/validate_workflows.py

validate: test check yaml