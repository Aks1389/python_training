# -*- coding: utf-8 -*-
from model.group import Group

def test_add_group(app):
    app.hm.session.login(username='admin', password='secret')
    app.hm.group.create(Group(name='group1', header='header1', footer='footer1'))
    app.hm.group.return_to_groups_page()
    app.hm.session.logout()

def test_add_empty_group(app):
    app.hm.session.login( username='admin', password='secret')
    app.hm.group.open_groups_page()
    app.hm.group.create(Group(name='', header='', footer=''))
    app.hm.group.return_to_groups_page()
    app.hm.session.logout()