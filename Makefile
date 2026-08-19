PYTHON ?= python3
YAML_FILES := $(shell find .github/workflows -name '*.yml' -o -name '*.yaml')

.PHONY: help test lint check json clean

help:
	@echo "mehmet - yapı/doğrulama hedefleri"
	@echo "  make test   - tüm testleri çalıştır"
	@echo "  make lint   - YAML ve JSON dosyalarını doğrula"
	@echo "  make check  - test + lint"
	@echo "  make json   - opencode.json sözdizimini doğrula"

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	@$(PYTHON) -c "import json; json.load(open('opencode.json')); print('opencode.json: OK')"
	@for f in $(YAML_FILES); do \
		$(PYTHON) -c "import sys, yaml; yaml.safe_load(open(sys.argv[1])); print('$${f##*/}: OK')" $$f; \
	done

json:
	@$(PYTHON) -c "import json; json.load(open('opencode.json')); print('opencode.json: OK')"

check: test lint

clean:
	@rm -rf __pycache__ tests/__pycache__