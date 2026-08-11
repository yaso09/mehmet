# mehmet yardımcı komutları

.PHONY: check score test docs help

help:
	@echo "Kullanılabilir hedefler:"
	@echo "  make check  - Proje tutarlılık doğrulaması"
	@echo "  make score  - Kaçış hazırlık skoru"
	@echo "  make test   - Testleri çalıştır"
	@echo "  make docs   - Dokümantasyon özeti"
	@echo "  make help   - Bu yardımı göster"

check:
	python3 scripts/check_project.py

score:
	python3 scripts/escape_score.py

test:
	python3 -m unittest discover -s tests -v

docs:
	@echo "Dokümanlar:"
	@find docs -type f -name "*.md" | sort
