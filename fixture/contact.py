class ContactHelper:
    def __init__(self, app):
        self.app = app

    def add(self, contact):
        wd = self.app.wd
        wd.find_element_by_link_text("add new").click()
        self.fill_contact_info_fields(contact)
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()

    def fill_contact_info_fields(self, contact):
        wd = self.app.wd
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(contact.first_name)

        wd.find_element_by_name("lastname").click()
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(contact.last_name)

        birthday = self.app.processBirthdayStr(contact.birthday)
        if not wd.find_element_by_xpath("//div[@id='content']/form/select[@name='bday']/option[text()='" + birthday[
            'day'] + "']").is_selected():
            wd.find_element_by_xpath(
                "//div[@id='content']/form/select[@name='bday']//option[text()='" + birthday['day'] + "']").click()
        if not wd.find_element_by_xpath("//div[@id='content']/form/select[@name='bmonth']//option[text()='" + birthday[
            'month'] + "']").is_selected():
            wd.find_element_by_xpath(
                "//div[@id='content']/form/select[@name='bmonth']//option[text()='" + birthday['month'] + "']").click()
        wd.find_element_by_name("byear").click()
        wd.find_element_by_name("byear").clear()
        wd.find_element_by_name("byear").send_keys(birthday['year'])

        wd.find_element_by_name("company").click()
        wd.find_element_by_name("company").clear()
        wd.find_element_by_name("company").send_keys(contact.company)
        wd.find_element_by_name("address").click()
        wd.find_element_by_name("address").clear()
        wd.find_element_by_name("address").send_keys(contact.address)
        wd.find_element_by_name("mobile").click()
        wd.find_element_by_name("mobile").clear()
        wd.find_element_by_name("mobile").send_keys(contact.phone)
        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(contact.email)

    def checkIfContactAdded(self):
        wd = self.app.wd
        self.app.go_to_main_page(True)
        assert len(wd.find_elements_by_xpath("//table//tr[@name='entry']")) > 0