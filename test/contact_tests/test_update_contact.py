# -*- coding: utf-8 -*-
from model.contact import Contact

def test_update_contact(app):
    app.contact.create_if_absent()
    app.contact.update(1, Contact("updated_userName1", "updated_lastName1", "17-May-1999",
                               "updated_address1", "007-18-45", "updated_email@email.com", "updated_companyName22"))