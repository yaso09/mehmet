.PHONY: check score health json help

# mehmet otomasyon hedefleri

## check | health — repo sağlık kontrolü + olgunluk skoru
check health:
	@bash scripts/health-check.sh

## score — yalnızca olgunluk skorunu yazdırır
score:
	@bash scripts/health-check.sh --score

## json — makine-okunabilir JSON raporu (CI için)
json:
	@bash scripts/health-check.sh --json

## help — kullanılabilir hedefleri listeler
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //'