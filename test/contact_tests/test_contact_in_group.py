from model.contact import Contact
from model.group import Group
import random

def test_add_contact_in_group(app, db, check_ui):
    new_contact = Contact(first_name="name_"+str(random.randint(1, 9999)), last_name="aosdksp"+str(random.randint(1, 9999)),
                          address="somewhere", birthday="25-November-1765")
    new_group = Group(name="superGroup"+str(random.randint(1, 9999)), header="abcd", footer="asd6577")

    old_contacts_list = db.get_contact_list()
    old_groups = db.get_group_list()
    #Create contact and check
    app.contact.add(new_contact)
    new_contacts_list = db.get_contact_list()
    old_contacts_list.append(new_contact)
    assert sorted(old_contacts_list, key=Contact.id_or_max) == sorted(new_contacts_list, key=Contact.id_or_max), \
        "Contact wasn't added"
    #Create group and check
    app.group.create(new_group)
    new_group.id = db.get_group_id(new_group)
    new_groups = db.get_group_list()
    old_groups.append(new_group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max) , \
        "Group wasn't added"

    #Add contact to the group
    app.contact.add_contact_to_group(new_contact, new_group)
    assert db.is_contact_in_group(new_contact, new_group) , "Contact wasn't added to the group"
    if check_ui:
        assert app.contact.is_contact_in_group(new_contact, new_group) , "Contact wasn't added to the group"

def test_remove_contact_from_group(app, db, check_ui):
    app.contact.create_if_absent()
    random_contact = random.choice(db.get_contact_list())

    app.group.create_if_absent()
    random_group = random.choice(db.get_group_list())

    if not db.is_contact_in_group(random_contact, random_group):
        app.contact.add_contact_to_group(random_contact, random_group)
        assert db.is_contact_in_group(random_contact, random_group), "Contact wasn't added to the group"

    app.contact.remove_from_group(random_contact, random_group)
    assert not db.is_contact_in_group(random_contact, random_group), "Contact wasn't removed from the group"
    if check_ui:
        app.contact.is_contact_in_group(random_contact, random_group)