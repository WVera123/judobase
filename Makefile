# Makefile

.PHONY: lint format test

SRC = "judobase/"

lint:
	ruff check $(SRC)
	flake8 $(SRC)

format:
	ruff format $(SRC)
	ruff check --fix $(SRC)

test:
	python -m pytest --cov --cov-fail-under=85
