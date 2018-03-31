# -*- coding: utf-8 -*-
from model.contact import Contact

def test_test_add_contact(app):
    old_contacts_list = app.contact.get_contact_list()
    contact = Contact(first_name="userName1", last_name="lastName1", birthday="13-November-1974",
                     address="address1", mobile_phone="247-18-45", email="email@email.com",
                     company="companyName21")
    app.contact.add(contact)

    new_contacts_list = app.contact.get_contact_list()
    assert len(old_contacts_list) + 1 == len(new_contacts_list), \
        "Contact wasn't added"
    old_contacts_list.append(contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"

def test_test_add_empty_contact(app):
    old_contacts_list = app.contact.get_contact_list()
    contact = Contact(first_name="", last_name="")
    app.contact.add(contact)

    new_contacts_list = app.contact.get_contact_list()
    assert len(old_contacts_list) + 1 == len(new_contacts_list), \
        "Contact wasn't added"
    old_contacts_list.append(contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"