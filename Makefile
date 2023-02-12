checks: lint test

lint:
	pylint $$(git ls-files '*.py')

test:
	python3 -m pytest -vv

mypy:
	mypy *.py --check-untyped-defs