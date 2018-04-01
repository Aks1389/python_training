# -*- coding: utf-8 -*-
from model.group import Group
import pytest
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [Group(name='', header='', footer='')] + [
    Group(name=random_string("name", 10), header=random_string("header", 10), footer=random_string("footer", 5))
    for i in range(5)
]

testdata2 = [
    Group(name=name, header=header, footer=footer)
    for name in ["", random_string("name", 10)]
    for header in ["", random_string("header", 10)]
    for footer in ["", random_string("footer", 10)]
]


@pytest.mark.parametrize("group", testdata2, ids=[repr(x) for x in testdata2])
def test_add_group(app, group):
    old_groups = app.group.get_group_list()

    app.group.create(group)

    # checking
    assert len(old_groups) + 1 == app.group.get_groups_number()
    new_groups = app.group.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)