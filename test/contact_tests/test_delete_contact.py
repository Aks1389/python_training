# -*- coding: utf-8 -*-
from model.contact import Contact

def test_delete_first_contact(app):
    app.contact.create_if_absent()
    contacts_before_del = app.contact.get_contact_list()

    app.contact.delete(1)

    contacts_after_del = app.contact.get_contact_list()
    assert len(contacts_before_del) - 1 == len(contacts_after_del), \
        "Number of contacts wasn't changed after deletion"
    del contacts_before_del[0]
    assert sorted(contacts_before_del, key=Contact.id_or_max) == sorted(contacts_after_del, key=Contact.id_or_max), \
        "Number of contacts wasn't changed after deletion"