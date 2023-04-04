checks: lint mypy test

lint:
	poetry run pylint $$(git ls-files '*.py')

mypy:
	poetry run mypy *.py --check-untyped-defs

test:
	poetry run python3 -m pytest -vv