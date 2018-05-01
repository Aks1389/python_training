from model.contact import Contact
from selenium.common.exceptions import NoSuchElementException
import re

class ContactHelper:
    contacts_cache = None
    table_header_map = None

    def __init__(self, app):
        self.app = app

    def add(self, contact):
        wd = self.app.wd

        wd.find_element_by_link_text("add new").click()
        self.fill_fields(contact)
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()
        self.contacts_cache = None

    def fill_fields(self, contact):
        wd = self.app.wd
        self.set_field_value(wd.find_element_by_name("firstname"), contact.first_name)
        self.set_field_value(wd.find_element_by_name("lastname"), contact.last_name)

        birthday = self.app.processDateStr(contact.birthday)

        cm_box_element = wd.find_element_by_xpath("//div[@id='content']/form/select[@name='bday']")
        self.set_combobox_field_value(cm_box_element, birthday['day'])

        cm_box_element = wd.find_element_by_xpath("//div[@id='content']/form/select[@name='bmonth']")
        self.set_combobox_field_value(cm_box_element, birthday['month'])

        cm_box_element = wd.find_element_by_xpath("//div[@id='content']/form/input[@name='byear']")
        self.set_field_value(cm_box_element, birthday['year'])

        self.set_field_value(wd.find_element_by_name("company"), contact.company)
        self.set_field_value(wd.find_element_by_name("address"), contact.address)
        self.set_field_value(wd.find_element_by_name("mobile"), contact.mobile_phone)
        self.set_field_value(wd.find_element_by_name("email"), contact.email)

    def checkIfContactAdded(self):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        assert len(wd.find_elements_by_xpath("//table//tr[@name='entry']")) > 0, \
            "Contact wasn't added"

    def get_contacts_number(self):
        wd = self.app.wd
        number = len(wd.find_elements_by_xpath("//table//tr[@name='entry']"))
        print("Number of contacts: " + str(number))
        return number

    def delete(self, index):
        wd = self.app.wd
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("//input[@value = 'Delete']").click()
        self.app.handleAlert("Delete 1 addresses?", "OK")
        self.contacts_cache = None

    def select_contact_by_index(self, index):
        wd = self.app.wd
        contact_list = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        assert len(contact_list) >= index , "Number of contacts is less than index"
        contact_list[index-1].find_element_by_xpath(".//input[@name = 'selected[]']").click()

    def select_contact_by_name(self, firstname, lastname):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        check_box = wd.find_element_by_xpath(
            "//tbody//tr//input[@title = 'Select (%s %s)']" % (firstname, lastname))
        if not check_box.is_selected():
            check_box.click()

    def update(self, index, contact):
        wd = self.app.wd

        #updating
        self.open_contact_for_editing(index)
        self.fill_fields(contact)
        wd.find_element_by_xpath("//input[@name = 'update']").click()
        self.contacts_cache = None

    def open_contact_for_editing(self, index):
        wd = self.app.wd
        contact_list = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        assert len(contact_list) >= index, "Number of contacts is less than index"
        wd.find_element_by_xpath("//table//tr["+str(index+1)+"]//a[contains(@href, 'edit.php')]").click()

    def open_contact_for_editing_by_name(self, firstname, lastname):
        wd = self.app.wd
        edit_btn = wd.find_element_by_xpath(
            "//tbody//input[@title = 'Select (%s %s)']//ancestor::tr//a[contains(@href, 'edit.php')]" % (firstname, lastname))
        edit_btn.click()

    def open_contact_for_view(self, index):
        wd = self.app.wd
        contact_list = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        assert len(contact_list) >= index, "Number of contacts is less than index"
        wd.find_element_by_xpath("//table//tr[" + str(index + 1) + "]//a[contains(@href, 'view.php')]").click()

    def set_field_value(self, web_element, field_obj):
        wd = self.app.wd
        if field_obj is not None:
            web_element.click()
            web_element.clear()
            web_element.send_keys(field_obj)

    def set_combobox_field_value(self, web_element, value):
        if value is not None:
            option = web_element.find_element_by_xpath("./option[text()='"+value+"']")
            if not option.is_selected():
                option.click()

    def display_contact_in_group(self, group_name):
        wd = self.app.wd
        web_element = wd.find_element_by_xpath("//select[@name = 'group']")
        self.set_combobox_field_value(web_element, group_name)

    def create_if_absent(self):
        self.app.go_to_main_page(True)
        self.display_contact_in_group("[all]")
        if self.get_contacts_number() == 0:
            self.add(Contact("userFirstName", "userLastName"))

    def get_contact_list(self):
        if(self.contacts_cache is None):
            wd = self.app.wd
            self.app.go_to_main_page(True)
            self.contacts_cache = []
            for row in wd.find_elements_by_xpath("//table//tr[@name='entry']"):
                self.contacts_cache.append(self.collect_info_about_contact(row))
            print("Contacts list: " + str(self.contacts_cache))
        else:
            self.app.go_to_main_page(True)
        return list(self.contacts_cache)

    def collect_info_about_contact(self, table_row):
        col_index = str(self.get_column_index("Last name") + 1)
        last_name = table_row.find_element_by_xpath(".//td[" + col_index + "]").text

        col_index = str(self.get_column_index("First name") + 1)
        first_name = table_row.find_element_by_xpath(".//td[" + col_index + "]").text

        col_index = str(self.get_column_index("Address") + 1)
        address = table_row.find_element_by_xpath(".//td[" + col_index + "]").text

        col_index = str(self.get_column_index("All e-mail") + 1)
        all_emails = list(map(lambda el: el.text, table_row.find_elements_by_xpath(".//td[" + col_index + "]/a")))

        id = table_row.find_element_by_xpath(".//input[@type='checkbox']").get_attribute("value")

        col_index = str(self.get_column_index("All phones") + 1)
        all_phones = table_row.find_element_by_xpath(".//td[" + col_index + "]").text

        return Contact(last_name=last_name, first_name=first_name, id=id,
                        address=address, all_emails=all_emails, all_phones=all_phones)

    def get_column_index(self, column_name):
        """wd = self.app.wd
        self.app.go_to_main_page(True)
        index = -1
        columns = wd.find_elements_by_xpath("//table//th")
        for i in range(len(columns)):
            if columns[i].text == column_name:
                index = i
                break
        return index"""
        self.init_table_header_map()
        return self.table_header_map[column_name]


    def init_table_header_map(self):
        if(self.table_header_map is None):
            wd = self.app.wd
            self.table_header_map = {}
            columns = wd.find_elements_by_xpath("//table//th")
            for i in range(len(columns)):
                try:
                    text = columns[i].find_element_by_xpath(".//*[text()]").text
                    self.table_header_map[text] = i
                except NoSuchElementException:
                    pass

    def get_contact_from_home_page(self, index):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        row = wd.find_element_by_xpath("//table//tr[@name='entry']["+str(index)+"]")
        return self.collect_info_about_contact(row)

    def get_all_contacts_from_home_page(self):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        rows = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        list = []
        for row in rows:
            list.append(self.collect_info_about_contact(row))
        return list

    def get_contact_from_edit_page(self, index):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        self.open_contact_for_editing(index)
        first_name = wd.find_element_by_name("firstname").get_attribute("value")
        last_name = wd.find_element_by_name("lastname").get_attribute("value")
        address = wd.find_element_by_name("address").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        all_emails = list(map(lambda el: el.get_attribute("value"),
                                wd.find_elements_by_xpath("//input[contains(@name, 'email')]")))
        home_phone = wd.find_element_by_name("home").get_attribute("value")
        mobile_phone = wd.find_element_by_name("mobile").get_attribute("value")
        work_phone = wd.find_element_by_name("work").get_attribute("value")
        secondary_phone = wd.find_element_by_name("phone2").get_attribute("value")
        return Contact(first_name=first_name, last_name=last_name, id=id,
                       home_phone=home_phone, mobile_phone=mobile_phone,
                       work_phone=work_phone, secondary_phone=secondary_phone,
                       address=address, all_emails=all_emails)

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        self.open_contact_for_view(index)
        text = wd.find_element_by_id("content").text
        home_phone = re.search("H: (.*)", text).group(1)
        mobile_phone = re.search("M: (.*)", text).group(1)
        work_phone = re.search("W: (.*)", text).group(1)
        secondary_phone = re.search("P: (.*)", text).group(1)
        return Contact(home_phone=home_phone, mobile_phone=mobile_phone,
                       work_phone=work_phone, secondary_phone=secondary_phone)

    def delete_contact(self, contact):
        wd = self.app.wd
        self.select_contact_by_name(contact.first_name, contact.last_name)
        wd.find_element_by_xpath("//input[@value = 'Delete']").click()
        self.app.handleAlert("Delete 1 addresses?", "OK")
        self.contacts_cache = None

    def update_contact(self, contact, new_contact_info):
        wd = self.app.wd
        # updating
        self.open_contact_for_editing_by_name(contact.first_name, contact.last_name)
        self.fill_fields(new_contact_info)
        wd.find_element_by_xpath("//input[@name = 'update']").click()
        self.contacts_cache = None

    def add_contact_to_group(self, contact, group):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        self.select_contact_by_name(contact.first_name, contact.last_name)
        web_element = wd.find_element_by_xpath("//select[@name = 'to_group']")
        self.set_combobox_field_value(web_element, group.name)
        wd.find_element_by_xpath("//input[@value = 'Add to']").click()
        self.app.go_to_main_page(True)

    def remove_from_group(self, contact, group):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        web_element = wd.find_element_by_xpath("//select[@name = 'group']")
        self.set_combobox_field_value(web_element, group.name)
        self.select_contact_by_name(contact.first_name, contact.last_name)
        wd.find_element_by_xpath("//input[@name = 'remove']").click()
        self.app.go_to_main_page(True)

    def is_contact_in_group(self, contact, group):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        self.display_contact_in_group(group.name)
        contacts = self.get_contact_list()
        return contact in contacts