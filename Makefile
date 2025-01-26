# Makefile

.PHONY: lint format

SRC = "judobase/"

lint:
	ruff check $(SRC)
	flake8 $(SRC)

format:
	ruff format $(SRC)
