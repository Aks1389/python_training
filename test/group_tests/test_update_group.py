# -*- coding: utf-8 -*-
from model.group import Group

def test_update_group(app):
    app.session.login(username='admin', password='secret')
    app.group.update(1, Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated'))
    app.group.return_to_groups_page()
    app.session.logout()