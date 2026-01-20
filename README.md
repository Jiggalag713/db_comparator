# dbComparator
Application for comparing mysql databases and viewing differences

1. Install PyCharm (it makes work easier)
2. Install python 3.10. Ubuntu:

```
sudo apt-get install python3
```

3. Install [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04) and [docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04).

4. Install mysql-server. Ubuntu:

```
sudo apt-get install mysql-server
```

5. Install pipx:

```
sudo apt-get install pipx
```

6. Install poetry 

```
pipx install poetry
```

7. Install dependencies

```
poetry install
```

8. Run script main_file.py.
9. Have fun.

To run comparator from command line
```
python3 headless.py --config /home/polter/PycharmProjects/db_comparator/resources/properties/1
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