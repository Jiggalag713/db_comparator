* [ ] configuration/sql_variables.py:35:13: W0511: TODO: [improve] adding serializing to html file on disc (fixme)
* [ ] configuration/sql_variables.py:10:1: W0511: TODO: potentially should be merged with table_data.Info (fixme)
* [ ] helpers/df_compare_helper.py:13:5: W0511: TODO: clarify, how I can dynamically set indexes for different tables (fixme)
* [ ] helpers/df_compare_helper.py:25:13: W0511: TODO: add logic for comparing non-identically labeled DataFrame object (fixme)
* [ ] helpers/df_compare_helper.py:40:5: W0511: TODO: clarify, how I can dynamically set indexes for different tables (fixme)
* [ ] helpers/df_compare_helper.py:52:9: W0511: TODO: add logic for comparing non-identically labeled DataFrame object (fixme)
* [ ] ui_elements/advanced_line_edits.py:11:9: W0511: TODO: [improve] add possibility for useful redacting of schema columns parameter (fixme)
* [ ] Pylint should be run before commit and shouldn't grant commit if errors. 
* [ ] Write abstract classes for ui elements, and inherit main and advanced window elements from this class (made them dataclasses)
Idea for abstract classes 2 methods. One of them should be set_tooltips
* [ ] Remove all stub function, refactor.
* [ ] [bug] Now during saving configuration to property file application mostly saves not values from ui, but from specific classes
* [ ] [bug] Seems like we not update class attributes after loading of property file. Fix in load method in existed mapping dicts
we should change to structure like {key: [ui.variable, instance.variable]} or use connections of ui elements to some variables
* [ ] Write unit tests for config_serialization module right after implementing of schema comparing
* [ ] If column list of some table differs, we should display this tables in exclude_table line edit, and disable ability to
set this tables unchecked.
* [ ] DefaultValues should be changed to Values
* [ ] mode parameter is not set
* [ ] configuration/sql_variables.py:21:5: W0511: TODO: [improve] strongly refactor this (fixme)
* [ ] df_helper string result = (prod_columns == test_columns) changed to result = True, check correctness of this
substitution
* [ ] Add unit tests for config_serialization

Windows backlog:

* [ ] configuration/system_config.py:58:13: W0511: TODO: [improve] add creation of directory below (fixme)
* [ ] configuration/system_config.py:59:13: W0511: TODO: [improve] check if disk C:/ is not exist (fixme)