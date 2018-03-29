from model.contact import Contact
from selenium.common.exceptions import NoSuchElementException

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
        self.set_field_value(wd.find_element_by_name("mobile"), contact.phone)
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

    def create_if_absent(self):
        self.app.go_to_main_page(True)
        if self.get_contacts_number() == 0:
            self.add(Contact("userFirstName", "userLastName"))

    def get_contact_list(self):
        if(self.contacts_cache is None):
            wd = self.app.wd
            self.app.go_to_main_page(True)
            self.contacts_cache = []
            for row in wd.find_elements_by_xpath("//table//tr[@name='entry']"):
                last_name = row.find_element_by_xpath(".//td[" + str(self.get_column_index("Last name")+1) + "]").text
                first_name = row.find_element_by_xpath(".//td["+ str(self.get_column_index("First name")+1)+"]").text
                id = row.find_element_by_xpath(".//input[@type='checkbox']").get_attribute("value")
                self.contacts_cache.append(Contact(last_name = last_name, first_name = first_name, id = id))
            print("Contacts list: " + str(self.contacts_cache))
        else:
            self.app.go_to_main_page(True)
        return list(self.contacts_cache)

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

