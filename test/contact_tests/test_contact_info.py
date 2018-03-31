import re
from random import randrange

def test_phone_on_home_page(app):
    contact_from_home_page = app.contact.get_contact_list()[0]
    contact_from_edit_page = app.contact.get_contact_from_edit_page(1)
    assert contact_from_home_page.all_phones == merge_phones_like_on_home_page(contact_from_edit_page)

def test_phone_on_view_page(app):
    contact_from_view_page = app.contact.get_contact_from_view_page(1)
    contact_from_edit_page = app.contact.get_contact_from_edit_page(1)
    assert contact_from_view_page.home_phone == contact_from_edit_page.home_phone
    assert contact_from_view_page.mobile_phone == contact_from_edit_page.mobile_phone
    assert contact_from_view_page.work_phone == contact_from_edit_page.work_phone
    assert contact_from_view_page.secondary_phone == contact_from_edit_page.secondary_phone

def test_contact_info(app):
    random_index = randrange(app.contact.get_contacts_number()) + 1
    print("Chosen contact: " + str(random_index))
    contact_from_home_page = app.contact.get_contact_from_home_page(random_index)
    contact_from_edit_page = app.contact.get_contact_from_edit_page(random_index)
    assert contact_from_home_page.first_name == contact_from_edit_page.first_name
    assert contact_from_home_page.last_name == contact_from_edit_page.last_name
    assert contact_from_home_page.address == contact_from_edit_page.address
    assert contact_from_home_page.all_phones == merge_phones_like_on_home_page(contact_from_edit_page)
    assert compare_emails_lists(contact_from_home_page.all_emails, contact_from_edit_page.all_emails)


def clear(s):
    return re.sub("[() -]", "", s)

def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x !="",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       (contact.home_phone, contact.mobile_phone, contact.work_phone, contact.secondary_phone)))))

def compare_emails_lists(email_list1, email_list2):
    #return sorted(filter(lambda x: x != "", email_list1)) == sorted(filter(lambda x: x != "", email_list2))
    return list(filter(lambda x: x != "", email_list1)) == list(filter(lambda x: x != "", email_list2))