# -*- coding: utf-8 -*-
from model.group import Group

def test_update_group(app):
    app.hm.session.login(username='admin', password='secret')
    app.hm.group.update(1, Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated'))
    app.hm.group.return_to_groups_page()
    app.hm.session.logout()