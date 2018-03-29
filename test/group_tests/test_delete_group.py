# -*- coding: utf-8 -*-
from model.group import Group

def test_delete_first_group(app):
    app.group.create_if_absent()

    groups_before_del = app.group.get_group_list()
    app.group.delete(1)

    # checking
    groups_after_del = app.group.get_group_list()
    assert len(groups_after_del) == len(groups_before_del) - 1, "Group wasn't deleted"
    del groups_before_del[0]
    assert sorted(groups_before_del, key=Group.id_or_max) == sorted(groups_after_del, key=Group.id_or_max)