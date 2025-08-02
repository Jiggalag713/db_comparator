checks: lint mypy test

run-it-tests: run-infra prepare-test-data tear-down

prepare-test-data: cleanup-test-data create-test-data

lint:
	poetry run pylint $$(git ls-files '*.py')

mypy:
	poetry run mypy $$(git ls-files '*.py') --check-untyped-defs --explicit-package-bases

test:
	poetry run python3 -m pytest -vv

create-test-data:
	 mysql -h localhost -P 33006 --protocol=tcp -u root -ptest1 < ./tests/resources/sql/fullfill_sql_data.sql

cleanup-test-data:
	 mysql -h localhost -P 33006 --protocol=tcp -u root -ptest1 < ./tests/resources/sql/cleanup_test_data.sql

run-infra:
	docker compose up -d --build

tear-down:
	docker compose down

mysql-local-connect:
	mysql -h localhost -P 33006 --protocol=tcp -u root -ptest1

mysql-show-databases:
	mysql -h localhost -P 33006 --protocol=tcp -u root -ptest1 -e "show databases;"