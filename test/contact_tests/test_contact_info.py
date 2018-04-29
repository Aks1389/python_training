import re

"""
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
"""
def test_all_contacts_info(app, db):
    all_contacts_from_home_page = sorted(app.contact.get_all_contacts_from_home_page(), key=lambda item: item.id)
    all_contacts_from_db = sorted(db.get_full_contacts_info(), key=lambda item: item.id)
    assert len(all_contacts_from_home_page) == len(all_contacts_from_db), "Length of the lists from ui and db is not the same"
    for i in range(len(all_contacts_from_home_page)):
        assert all_contacts_from_home_page[i].first_name == all_contacts_from_db[i].first_name
        assert all_contacts_from_home_page[i].last_name == all_contacts_from_db[i].last_name
        assert all_contacts_from_home_page[i].address == all_contacts_from_db[i].address
        assert all_contacts_from_home_page[i].all_phones == \
               format_phones_number_according_to_ui_rules(all_contacts_from_db[i].all_phones)
        assert compare_emails_lists(all_contacts_from_home_page[i].all_emails, all_contacts_from_db[i].all_emails.split("\n"))

def clear(s):
    return re.sub("[() -]", "", s)

def format_phones_number_according_to_ui_rules(number):
    return clear(re.sub("^[0]{2}", "+", number.strip('\n')))

def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x !="",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       (contact.home_phone, contact.mobile_phone, contact.work_phone, contact.secondary_phone)))))

def compare_emails_lists(email_list1, email_list2):
    #return sorted(filter(lambda x: x != "", email_list1)) == sorted(filter(lambda x: x != "", email_list2))
    return list(filter(lambda x: x != "", email_list1)) == list(filter(lambda x: x != "", email_list2))