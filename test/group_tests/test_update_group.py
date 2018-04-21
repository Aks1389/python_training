# -*- coding: utf-8 -*-
from model.group import Group
import random

def test_update_group(app, db, check_ui):
    app.group.create_if_absent()
    # preparation
    new_group = Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated')
    old_groups = db.get_group_list()
    random_group = random.choice(old_groups)
    new_group.id = random_group.id

    app.group.update_by_id(random_group.id, new_group)

    # checking
    new_groups = db.get_group_list()
    # replacing old contact which was updated
    for n in range(len(old_groups)):
        if old_groups[n].id == new_group.id:
            old_groups[n] = new_group
            break
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)