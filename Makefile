.PHONY: help check maturity escape

help:
	@echo "Kullanilabilir hedefler:"
	@echo "  make check     - yapisal dogrulama kontrollerini calistir"
	@echo "  make maturity  - kacis/olgunluk skorunu raporla"
	@echo "  make escape    - kacis durumunu degerlendir (maturity ile ayni)"

check:
	bash scripts/check.sh

maturity:
	bash scripts/maturity.sh

escape:
	bash scripts/maturity.sh