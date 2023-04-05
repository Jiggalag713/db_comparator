checks: lint mypy test

lint:
	poetry run pylint $$(git ls-files '*.py')

mypy:
	poetry run mypy *.py --check-untyped-defs

test:
	poetry run python3 -m pytest -vv

cmp-up:
	docker-compose up -d

cmp-down:
	docker-compose down

prepare-test-data:
	 mysql -h localhost -P 33006 --protocol=tcp -u root -ptest1 < ./tests/fullfill_sql_data.sql