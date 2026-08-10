.PHONY: check test validate maturity

# mehmet geliştirme araçları
# Tüm kalite kapılarını tek komutla çalıştır: make check

test:            ## Unit testlerini çalıştır
	python3 -m unittest discover -s tests -v

validate:        ## Yapısal doğrulama yap
	python3 scripts/validate.py

maturity:        ## Olgunluk raporunu üret
	python3 scripts/maturity.py

check: test validate maturity  ## Test + doğrulama + olgunluk raporu