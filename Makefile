.PHONY: maturity test check help

help: ## Bu yardımı göster
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

maturity: ## Olgunluk raporunu göster
	@scripts/check-maturity.sh

test: ## Test altyapısını çalıştır
	@scripts/test-maturity.sh

check: maturity test ## Tüm kontrolleri çalıştır (maturity + test)
	@echo "make check tamamlandı."