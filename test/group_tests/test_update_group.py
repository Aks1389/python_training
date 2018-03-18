# -*- coding: utf-8 -*-
from model.group import Group

def test_update_group(app):
    app.group.create_if_absent()
    app.group.update(1, Group(name='groupUpdated', header='headerUpdated', footer='footerUpdated'))