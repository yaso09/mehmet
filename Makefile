.PHONY: help check test maturity

help:
	@echo "make check     - konfigürasyon ve script sözdizimini doğrula"
	@echo "make test      - script sözdizimi + opencode.json doğrulama"
	@echo "make maturity  - olgunluk (kaçış) skorunu hesapla"

check: test maturity

test:
	@bash -n scripts/*.sh
	@python3 -c "import json; json.load(open('opencode.json'))"
	@echo "OK: tüm denetimler geçti"

maturity:
	@bash scripts/maturity.sh
