# -*- coding: utf-8 -*-
from model.group import Group

def test_add_group(app):
    app.group.create(Group(name='group1', header='header1', footer='footer1'))
    app.group.return_to_groups_page()

def test_add_empty_group(app):
    app.group.open_groups_page()
    app.group.create(Group(name='', header='', footer=''))
    app.group.return_to_groups_page()