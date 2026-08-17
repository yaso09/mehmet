.PHONY: validate changelog plan check

# Validate that AGENTS.md simulation rules are followed
validate:
	@./scripts/validate.sh

# Show changelog
changelog:
	@cat CHANGELOG.md

# Show escape progress (maturity score)
plan:
	@echo "=== Maturity / Kacis Durumu ==="
	@grep -A2 'Toplam' MATURITY.md | head -3

# Full health check (validate + shellcheck on scripts)
check: validate
	@command -v shellcheck >/dev/null 2>&1 && shellcheck scripts/validate.sh && echo "shellcheck OK" || echo "shellcheck yok, atlaniyor"