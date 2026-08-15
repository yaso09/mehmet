.PHONY: check maturity test all

check:            ## Proje bütünlüğünü doğrula
	bash scripts/check.sh

maturity:         ## Olgunluk skorunu ve seviyeyi göster
	bash scripts/maturity.sh

test:             ## Test altyapısını çalıştır
	bash scripts/test.sh

all: check maturity test