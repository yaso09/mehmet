# mehmet — standart komutlar
# Kullanım: make <hedef>   (bkz. `make help`)

SHELL := /bin/bash
MDL := $(shell command -v markdownlint-cli2 2>/dev/null || command -v markdownlint 2>/dev/null || echo "")
YAML_LINT := $(shell command -v yamllint 2>/dev/null || echo "")
SHELLCHECK := $(shell command -v shellcheck 2>/dev/null || echo "")

.PHONY: help check lint yaml-lint markdown-lint shell-lint escape test ci

help: ## Kullanılabilir komutları listele
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

check: ## Tüm kalite kontrollerini çalıştır
	@$(MAKE) lint
	@$(MAKE) escape

escape: ## Kaçış hazırlık skorunu göster
	@./scripts/check-escape-ready.sh

lint: markdown-lint yaml-lint shell-lint ## Tüm lint'leri çalıştır

markdown-lint: ## Markdown dosyalarını denetle
	@if [ -n "$(MDL)" ]; then \
		$(MDL) '**/*.md' --fix 2>/dev/null || $(MDL) '**/*.md'; \
	else \
		echo "UYARI: markdownlint kurulu değil (npx markdownlint-cli2 --fix '**/*.md')."; \
	fi

yaml-lint: ## YAML dosyalarını denetle
	@if [ -n "$(YAML_LINT)" ]; then \
		yamllint .github/workflows/; \
	else \
		echo "UYARI: yamllint kurulu değil."; \
	fi

shell-lint: ## Shell script'lerini denetle
	@if [ -n "$(SHELLCHECK)" ]; then \
		shellcheck scripts/*.sh; \
	else \
		echo "UYARI: shellcheck kurulu değil."; \
	fi

test: ## Testleri çalıştır (escape script'i dahil)
	@bash scripts/check-escape-ready.sh --strict

ci: ## CI'da kullanılan hızlı doğrulama
	@$(MAKE) markdown-lint
	@$(MAKE) yaml-lint
	@$(MAKE) shell-lint
	@$(MAKE) escape
