# -*- coding: utf-8 -*-
from model.group import Group
from random import randrange

def test_update_group(app):
    app.group.create_if_absent()
    # preparation
    group = Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated')
    old_groups = app.group.get_group_list()
    random_index = randrange(len(old_groups)) + 1
    group.id = old_groups[random_index-1].id

    app.group.update(random_index, group)

    # checking
    assert len(old_groups) == app.group.get_groups_number()
    new_groups = app.group.get_group_list()
    old_groups[random_index-1] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)