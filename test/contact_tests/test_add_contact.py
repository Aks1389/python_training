# -*- coding: utf-8 -*-
from model.contact import Contact

def test_test_add_contact(app):
    app.hm.session.login(username='admin', password='secret')
    app.hm.contact.add(Contact("userName1", "lastName1", "13-November-1974",
                            "address1", "247-18-45", "email@email.com", "companyName21"))
    app.hm.contact.checkIfContactAdded()
    app.hm.session.logout()
