# -*- coding: utf-8 -*-
from model.contact import Contact

def test_test_add_contact(app, db, json_contacts, check_ui):
    contact = json_contacts
    old_contacts_list = db.get_contact_list()
    app.contact.add(contact)
    new_contacts_list = db.get_contact_list()
    old_contacts_list.append(contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"
    if check_ui:
        assert sorted(new_contacts_list, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max), \
            "Contact wasn't added"