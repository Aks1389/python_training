# -*- coding: utf-8 -*-
from model.group import Group
import random

def test_delete_random_group(app, db, check_ui):
    app.group.create_if_absent()

    groups_before_del = db.get_group_list()
    group = random.choice(groups_before_del)
    app.group.delete_by_id(group.id)

    # checking
    groups_after_del = db.get_group_list()
    assert len(groups_after_del) == len(groups_before_del) - 1, "Group wasn't deleted"
    groups_before_del.remove(group)
    assert sorted(groups_before_del, key=Group.id_or_max) == sorted(groups_after_del, key=Group.id_or_max)
    if check_ui:
        assert sorted(groups_after_del, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)