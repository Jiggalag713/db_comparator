# dbComparator
Application for comparing mysql databases and viewing differences

1. Install PyCharm (it makes work easier)
2. Install python 3.10. Ubuntu:
sudo apt-get install python3
3. Install poetry 

```
curl -sSL https://install.python-poetry.org | python3 -
```

4. Install dependencies

```
poetry install
```

5. Run script main_file.py.
6. Have fun.

To run comparator from command line
```
python3 headles..py --config /home/polter/PycharmProjects/db_comparator/resources/properties/1
```

Run pylint

```
make lint
```

Run mypy-checks

```
make mypy
```

Run tests

```
make test
```

Sequence run pylint, mypy, pytest:

```
make checks
```

Run integration tests(in docker-compose):

```
make run-it-tests
```

view it-tests report:
# TODO

shut down it-test compose:

```
make tear-down
```