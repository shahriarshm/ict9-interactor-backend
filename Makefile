.PHONY: format lint test

format:
	black .

lint:
	flake8 .

test:
	python -m pytest

check: format lint test
