.PHONY: verify test help

verify: ## Proje sağlık kontrollerini çalıştır
	sh scripts/verify.sh

test: verify ## Test ve doğrulama adımlarını çalıştır
	@echo "Otomatik test altyapısı henüz mevcut değil."

help: ## Bu yardımı göster
	@grep -E '^[a-zA-Z_-]+:.*## ' Makefile | awk 'BEGIN {FS = ":.*## "}; {printf "  %-10s %s\n", $$1, $$2}'