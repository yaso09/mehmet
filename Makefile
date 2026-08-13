.PHONY: validate test score doctor help

help: ## Bu yardımı göster
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

validate: ## Proje bütünlüğünü doğrula (CI'da çalışır)
	@bash scripts/validate.sh

test: validate ## Test = doğrulama (yeni testler eklendikçe genişler)

score: ## Olgunluk skorunu göster
	@bash scripts/score.sh 2>/dev/null || echo "MATURITY.md skor satırını görüntüleyin (aşağıda):"
	@grep -E "^\| [0-9]{4}-" MATURITY.md | tail -1

doctor: validate ## Sistemi kontrol et ve raporla
	@echo "Shell: $$(command -v bash)"
	@echo "Python: $$(python3 --version 2>/dev/null || echo 'yok')"
	@echo "Git: $$(git --version)"
