.PHONY: health validate test check

## Healthcheck raporunu goster
health:
	python3 scripts/healthcheck.py

## Dogrulama: healthcheck'i esik degeriyle calistir
validate:
	python3 scripts/healthcheck.py --fail-below 70

## Birim testleri calistir
test:
	python3 -m unittest discover -s tests -v

## Test + dogrulama
check: test validate