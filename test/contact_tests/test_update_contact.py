# -*- coding: utf-8 -*-
from model.contact import Contact

def test_update_contact(app):
    app.session.login(username='admin', password='secret')
    app.contact.update(1, Contact("updated_userName1", "updated_lastName1", "17-May-1999",
                               "updated_address1", "007-18-45", "updated_email@email.com", "updated_companyName22"))
    app.go_to_main_page(True)
    app.session.logout()