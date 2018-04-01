# -*- coding: utf-8 -*-
from model.contact import Contact
import pytest
import random
import string
import datetime
import re

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_phone():
    return "+"+random.choice(string.digits)+"".join([random.choice(string.digits + " "*7) for i in range(11)])

def random_date():
    date = (datetime.date.today() - datetime.timedelta(days=random.randint(0,29999))).strftime("%d-%B-%Y")
    return re.sub("^0","", date)

def random_email():
    symbols = string.ascii_letters + string.digits
    return "".join([random.choice(symbols) for i in range(random.randrange(10))])+ "@" + \
           "".join([random.choice(symbols) for i in range(random.randrange(4))]) + ".com"


testdata = [Contact(first_name="", last_name="")] + [
    Contact(first_name=random_string("name", 7), last_name=random_string("", 12), birthday=random_date(),
            address=random_string("street ", 15), mobile_phone=random_phone(), email=random_email(),
            company=random_string("comp.", 10))
    for i in range(5)
]

@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_test_add_contact(app, contact):
    old_contacts_list = app.contact.get_contact_list()
    app.contact.add(contact)

    new_contacts_list = app.contact.get_contact_list()
    assert len(old_contacts_list) + 1 == len(new_contacts_list), \
        "Contact wasn't added"
    old_contacts_list.append(contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"
"""
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
"""