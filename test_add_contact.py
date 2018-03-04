# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
import unittest
from contact import Contact
from personal_info import PersonalInfo
from contact_info import ContactInfo

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

def processBirthdayStr(birthdayStr):
    bd_string = str.split(birthdayStr, '-')
    birthdayDict = {'day' : bd_string[0],
                    'month' : bd_string[1],
                    'year' : bd_string[2]}
    return birthdayDict

class test_add_contact(unittest.TestCase):
    def setUp(self):
        self.wd = WebDriver(capabilities={"marionette": False})
        self.wd.implicitly_wait(20)
    
    def test_test_add_contact(self):
        wd = self.wd
        self.go_to_main_page(wd, False)
        self.login(wd, username='admin', password='secret')
        self.add_contact(wd, Contact(PersonalInfo("userName1", "lastName1", "13-November-1974"),
                                     ContactInfo("address1", "247-18-45", "email@email.com", "companyName21")))
        self.go_to_main_page(wd, True)
        self.checkIfContactAdded(wd)
        self.logout(wd)

    def go_to_main_page(self, wd, byLink):
        if byLink:
            wd.find_element_by_link_text("home").click()
        else:
            wd.get("http://localhost/addressbook/")

    def login(self, wd, username, password):
        wd.find_element_by_id("content").click()
        wd.find_element_by_name("user").click()
        wd.find_element_by_name("user").clear()
        wd.find_element_by_name("user").send_keys(username)
        wd.find_element_by_name("pass").click()
        wd.find_element_by_name("pass").clear()
        wd.find_element_by_name("pass").send_keys(password)
        wd.find_element_by_xpath("//form[@id='LoginForm']/input[@type='submit']").click()

    def add_contact(self, wd, contact):
        wd.find_element_by_link_text("add new").click()
        self.fill_personal_info_fields(wd, contact.personal_info)
        self.fill_contact_info_fields(wd, contact.contact_info)
        wd.find_element_by_xpath("//div[@id='content']/form/input[@value='Enter']").click()

    def fill_personal_info_fields(self, wd, personal_info):
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(personal_info.first_name)

        wd.find_element_by_name("lastname").click()
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(personal_info.last_name)

        birthday = processBirthdayStr(personal_info.birthday)
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

    def fill_contact_info_fields(self, wd, contact_info):
        wd.find_element_by_name("company").click()
        wd.find_element_by_name("company").clear()
        wd.find_element_by_name("company").send_keys(contact_info.company)
        wd.find_element_by_name("address").click()
        wd.find_element_by_name("address").clear()
        wd.find_element_by_name("address").send_keys(contact_info.address)
        wd.find_element_by_name("mobile").click()
        wd.find_element_by_name("mobile").clear()
        wd.find_element_by_name("mobile").send_keys(contact_info.phone)
        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(contact_info.email)

    def checkIfContactAdded(self, wd):
        assert len(wd.find_elements_by_xpath("//table//tr[@name='entry']")) > 0

    def logout(self, wd):
        wd.find_element_by_link_text("Logout").click()

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
