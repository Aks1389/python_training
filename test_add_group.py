# -*- coding: utf-8 -*-
from application import Application
import pytest
from group import Group

@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture

def test_add_group(app):
    app.login(username='admin', password='secret')
    app.create_new_group(Group(name='group1', header='header1', footer='footer1'))
    app.return_to_groups_page()
    app.logout()

def test_add_empty_group(app):
    app.login( username='admin', password='secret')
    app.open_groups_page()
    app.create_new_group(Group(name='', header='', footer=''))
    app.return_to_groups_page()
    app.logout()