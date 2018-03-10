from selenium.webdriver.firefox.webdriver import WebDriver

class Application:
    def __init__(self):
        self.wd = WebDriver(capabilities={"marionette": False})
        self.wd.implicitly_wait(20)

    def go_to_main_page(self, byLink):
        wd = self.wd
        if byLink:
            wd.find_element_by_link_text("home").click()
        else:
            wd.get("http://localhost/addressbook/")

    def login(self, username, password):
        wd = self.wd
        self.go_to_main_page(False)
        wd.find_element_by_id("content").click()
        wd.find_element_by_name("user").click()
        wd.find_element_by_name("user").clear()
        wd.find_element_by_name("user").send_keys(username)
        wd.find_element_by_name("pass").click()
        wd.find_element_by_name("pass").clear()
        wd.find_element_by_name("pass").send_keys(password)
        wd.find_element_by_xpath("//form[@id='LoginForm']/input[@type='submit']").click()

    def add_contact(self, contact):
        wd = self.wd
        wd.find_element_by_link_text("add new").click()
        self.fill_contact_info_fields(contact)
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()

    def fill_contact_info_fields(self, contact):
        wd = self.wd
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(contact.first_name)

        wd.find_element_by_name("lastname").click()
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(contact.last_name)

        birthday = self.processBirthdayStr(contact.birthday)
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
        wd = self.wd
        self.go_to_main_page(True)
        assert len(wd.find_elements_by_xpath("//table//tr[@name='entry']")) > 0

    def logout(self):
        wd = self.wd
        wd.find_element_by_link_text("Logout").click()

    def return_to_groups_page(self):
        wd = self.wd
        wd.find_element_by_link_text("group page").click()

    def create_new_group(self, group):
        wd = self.wd
        self.open_groups_page()
        wd.find_element_by_name("group_name").click()
        # fill group form
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys(group.name)
        wd.find_element_by_name("group_header").click()
        wd.find_element_by_name("group_header").clear()
        wd.find_element_by_name("group_header").send_keys(group.header)
        wd.find_element_by_name("group_footer").click()
        wd.find_element_by_name("group_footer").clear()
        wd.find_element_by_name("group_footer").send_keys(group.footer)
        # submit group creating
        wd.find_element_by_name("submit").click()

    def open_groups_page(self):
        # open groups page
        wd = self.wd
        wd.find_element_by_link_text("groups").click()
        wd.find_element_by_name("new").click()

    def destroy(self):
        self.wd.quit()

    def processBirthdayStr(self, birthdayStr):
        bd_string = str.split(birthdayStr, '-')
        birthdayDict = {'day' : bd_string[0],
                        'month' : bd_string[1],
                        'year' : bd_string[2]}
        return birthdayDict