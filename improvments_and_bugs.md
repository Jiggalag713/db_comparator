* [ ] configuration/sql_variables.py:35:13: W0511: TODO: [improve] adding serializing to html file on disc (fixme)
* [ ] helpers/df_compare_helper.py:13:5: W0511: TODO: clarify, how I can dynamically set indexes for different tables (fixme)
* [ ] helpers/df_compare_helper.py:25:13: W0511: TODO: add logic for comparing non-identically labeled DataFrame object (fixme)
* [ ] Pylint should be run before commit and shouldn't grant commit if errors.
* [ ] Write abstract classes for ui elements, and inherit main and advanced window elements from this class (made them dataclasses)
Idea for abstract classes 2 methods. One of them should be set_tooltips
* [ ] Remove all stub function, refactor.
we should change to structure like {key: [ui.variable, instance.variable]} or use connections of ui elements to some variables
* [ ] df_helper string result = (prod_columns == test_columns) changed to result = True, check correctness of this
substitution
* [ ] Add test stage to github actions
* [ ] split ui and logic: buttons
* [ ] try to add black
* [ ] test "most cruel linter" from habr

Windows backlog:

* [ ] configuration/system_config.py:58:13: W0511: TODO: [improve] add creation of directory below (fixme)
* [ ] configuration/system_config.py:59:13: W0511: TODO: [improve] check if disk C:/ is not exist (fixme)
