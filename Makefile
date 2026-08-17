.PHONY: check maturity

# Proje bütünlük ve olgunluk kontrolü
check: maturity

maturity:
	bash scripts/maturity_check.sh