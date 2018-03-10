# -*- coding: utf-8 -*-
from application import Application
import pytest
from contact import Contact

@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture

def test_test_add_contact(app):
    app.login(username='admin', password='secret')
    app.add_contact(Contact("userName1", "lastName1", "13-November-1974",
                            "address1", "247-18-45", "email@email.com", "companyName21"))
    app.checkIfContactAdded()
    app.logout()
