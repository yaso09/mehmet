.PHONY: check health lint test clean

# mehmet gelistirme komutlari

## Sağlık ve olgunluk kontrolü
check health:
	python3 scripts/healthcheck.py

## Sözdizimi kontrolü (sadece doğrulama amaçlı, bağımlılık yok)
lint:
	python3 -m py_compile scripts/healthcheck.py

## Yapıcı testler
test: lint
	python3 -m unittest discover -s tests -v
	python3 scripts/healthcheck.py

## Python bytecode artıklarını temizle
clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
