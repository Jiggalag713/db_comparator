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