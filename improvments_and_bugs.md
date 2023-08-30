* [ ] Pylint should be run before commit and shouldn't grant commit if errors found.
* [ ] Write abstract classes for ui elements, and inherit main and advanced window elements from this class (made them dataclasses)
Idea for abstract classes 2 methods. One of them should be set_tooltips
* [ ] Remove all stub function, refactor.
we should change to structure like {key: [ui.variable, instance.variable]} or use connections of ui elements to some variables
* [ ] df_helper string result = (prod_columns == test_columns) changed to result = True, check correctness of this
substitution
* [ ] try to add black
* [ ] Add integration tests. Prepare docker-container with mysql-server, databases with test data and code.

Windows backlog:

* [ ] configuration/system_config.py:58:13: W0511: TODO: [improve] add creation of directory below (fixme)
* [ ] configuration/system_config.py:59:13: W0511: TODO: [improve] check if disk C:/ is not exist (fixme)

docker_compose:

1. Configure mysql-server.
2. Configure comparator-container.