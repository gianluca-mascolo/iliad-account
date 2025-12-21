.DEFAULT_GOAL := run

.PHONY: run fmt

run:
	poetry run iliad_account

fmt:
	poetry run isort .
	poetry run black .
	poetry run flake8 .
