.PHONY: test check maturity

# Test altyapısını çalıştırır
test:
	python3 -m unittest discover -s tests -v

# Tüm doğrulamaları çalıştırır (test + olgunluk)
check: test
	python3 scripts/maturity.py

# Olgunluk skorunu makine okunur formatta raporlar
maturity:
	python3 scripts/maturity.py --json