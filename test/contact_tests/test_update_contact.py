# -*- coding: utf-8 -*-
from model.contact import Contact
from random import randrange

def test_update_contact(app):
    app.contact.create_if_absent()
    # preparation
    contact = Contact("updated_userName1", "updated_lastName1", "17-May-1999",
                               "updated_address1", "007-18-45", "updated_email@email.com", "updated_companyName22")
    old_contacts_list = app.contact.get_contact_list()
    random_index = randrange(len(old_contacts_list))+1
    contact.id = old_contacts_list[random_index-1].id
    app.contact.update(random_index, contact)

    # checking
    new_contacts_list = app.contact.get_contact_list()
    assert len(old_contacts_list) == len(new_contacts_list), \
        "Number of contacts changed after contact updating"
    old_contacts_list[random_index-1] = contact
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Number of contacts changed after contact updating"