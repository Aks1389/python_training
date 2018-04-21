# -*- coding: utf-8 -*-
from model.contact import Contact
import random

def test_update_contact(app, db, check_ui):
    app.contact.create_if_absent()
    # preparation
    new_contact = Contact(first_name="updated_userName1", last_name="updated_lastName1", birthday="17-May-1999",
                      address="updated_address1", mobile_phone="007-18-45", email="updated_email@email.com",
                      company="updated_companyName22")
    old_contacts_list = db.get_contact_list()
    #random_index = randrange(len(old_contacts_list))+1
    random_contact = random.choice(old_contacts_list)
    new_contact.id = random_contact.id
    app.contact.update_contact(random_contact, new_contact)

    # checking
    new_contacts_list = db.get_contact_list()
    assert len(old_contacts_list) == len(new_contacts_list), \
        "Number of contacts changed after contact updating"
    #replacing old contact which was updated
    for n in range(len(old_contacts_list)):
        if old_contacts_list[n].id == new_contact.id:
            old_contacts_list[n] = new_contact
            break
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Number of contacts changed after contact updating"
    if check_ui:
        assert sorted(new_contacts_list, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)