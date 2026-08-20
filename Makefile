SHELL := /bin/bash
.PHONY: help validate status all

help: ## Kullanılabilir hedefleri listele
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## Proje tutarlılığını doğrula
	python3 scripts/validate.py

status: ## Kaçış olgunluk skorunu hesapla
	python3 scripts/escape_status.py

all: validate status ## Tüm kontrolleri çalıştır