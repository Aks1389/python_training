class ContactHelper:
    def __init__(self, app):
        self.app = app

    def add(self, contact):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()
        self.fill_fields(contact)
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()

    def add_empty(self):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()

    def fill_fields(self, contact):
        wd = self.app.wd
        self.set_field_value(wd.find_element_by_name("firstname"), contact.first_name)
        self.set_field_value(wd.find_element_by_name("lastname"), contact.last_name)

        birthday = self.app.processDateStr(contact.birthday)

        cm_box_element = wd.find_element_by_xpath("//div[@id='content']"
                                                  "/form/select[@name='bday']"
                                                  "/option[text()='" + birthday['day'] + "']")
        self.set_combobox_field_value(cm_box_element, birthday['day'])

        cm_box_element = wd.find_element_by_xpath("//div[@id='content']"
                                                  "/form/select[@name='bmonth']"
                                                  "//option[text()='" + birthday['month'] + "']")
        self.set_combobox_field_value(cm_box_element, birthday['day'])

        self.set_field_value(wd.find_element_by_name("byear"), birthday['year'])

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
        self.app.go_to_main_page(True)
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("//input[@value = 'Delete']").click()
        self.app.handleAlert("Delete 1 addresses?", "OK")

    def select_contact_by_index(self, index):
        wd = self.app.wd
        contact_list = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        assert len(contact_list) >= index , "Number of contacts is less than index"
        contact_list[index-1].find_element_by_xpath(".//input[@name = 'selected[]']").click()

    def update(self, index, contact):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        self.open_contact_for_editing(index)
        self.fill_fields(contact)
        wd.find_element_by_xpath("//input[@name = 'update']").click()

    def open_contact_for_editing(self, index):
        wd = self.app.wd
        contact_list = wd.find_elements_by_xpath("//table//tr[@name='entry']")
        assert len(contact_list) >= index, "Number of contacts is less than index"
        wd.find_element_by_xpath("//table//tr["+str(index+1)+"]//a[contains(@href, 'edit.php')]").click()

    def set_field_value(self, web_element, value):
        wd = self.app.wd
        web_element.click()
        web_element.clear()
        web_element.send_keys(value)

    def set_combobox_field_value(self, web_element, value):
        if not web_element.is_selected():
            web_element.click()