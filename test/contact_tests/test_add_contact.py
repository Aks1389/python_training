# -*- coding: utf-8 -*-
from model.contact import Contact

def test_test_add_contact(app):
    app.contact.add(Contact("userName1", "lastName1", "13-November-1974",
                            "address1", "247-18-45", "email@email.com", "companyName21"))

def test_test_add_empty_contact(app):
    app.contact.add_empty()