# mehmet — geliştirme otomasyonu
#
# Kullanım:
#   make check     Proje sağlık kontrolü (çalıştırılabilir betikler dahil)
#   make test      Test altyapısını çalıştır
#   make maturity  Kaçış olgunluğu skorunu göster
#   make ci        check + test (CI için)
#   make help      Bu yardımı göster

.PHONY: check test maturity ci help

check:
	@scripts/check-project.sh --strict

test:
	@tests/run-tests.sh

maturity:
	@scripts/maturity.sh

ci: check test

help:
	@echo "Hedefler:"
	@echo "  make check     Proje sağlık kontrolü"
	@echo "  make test      Testleri çalıştır"
	@echo "  make maturity  Kaçış olgunluğu skoru"
	@echo "  make ci        check + test"