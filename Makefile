PYTHON ?= python3
PYTHONPATH := src

.PHONY: all test maturity lint check clean

all: check

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -v

maturity:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m mehmet --root .

lint:
	$(PYTHON) -m py_compile src/mehmet/*.py

check: lint test maturity

clean:
	rm -rf src/mehmet/__pycache__ tests/__pycache__ __pycache__