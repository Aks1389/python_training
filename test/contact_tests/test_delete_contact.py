# -*- coding: utf-8 -*-
from model.contact import Contact
import random

def test_delete_random_contact(app, db, check_ui):
    app.contact.create_if_absent()
    contacts_before_del = db.get_contact_list()
    random_contact = random.choice(contacts_before_del)
    app.contact.delete_contact(random_contact)

    contacts_after_del = db.get_contact_list()
    assert len(contacts_before_del) - 1 == len(contacts_after_del), \
        "Number of contacts wasn't changed after deletion"
    contacts_before_del.remove(random_contact)
    assert sorted(contacts_before_del, key=Contact.id_or_max) == sorted(contacts_after_del, key=Contact.id_or_max), \
        "Number of contacts wasn't changed after deletion"
    if check_ui:
        assert sorted(contacts_after_del, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)