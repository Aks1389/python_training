# -*- coding: utf-8 -*-
from model.group import Group

def test_update_group(app):
    app.group.create_if_absent()
    # preparation
    group = Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated')
    old_groups = app.group.get_group_list()
    group.id = old_groups[0].id

    app.group.update(1, group)

    # checking
    assert len(old_groups) == app.group.get_groups_number()
    new_groups = app.group.get_group_list()
    old_groups[0] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)