# -*- coding: utf-8 -*-
from model.contact import Contact

def test_test_add_contact(app, json_contacts):
    contact = json_contacts
    old_contacts_list = app.contact.get_contact_list()
    app.contact.add(contact)
    new_contacts_list = app.contact.get_contact_list()
    assert len(old_contacts_list) + 1 == len(new_contacts_list), \
        "Contact wasn't added"
    old_contacts_list.append(contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"