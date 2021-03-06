from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from fixture.session import SessionHelper
from fixture.contact import ContactHelper
from fixture.group import GroupHelper

class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(capabilities={"marionette": False})
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "opera":
            self.wd = webdriver.Opera()
        elif browser == "edge":
            self.wd = webdriver.Edge()
        else :
            raise ValueError("Unrecognized browser %s", browser)
        self.session = SessionHelper(self)
        self.contact = ContactHelper(self)
        self.group = GroupHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def go_to_main_page(self, byLink):
        wd = self.wd
        if not wd.current_url.endswith("addressbook/"):
            if byLink:
                wd.find_element_by_link_text("home").click()
            else:
                wd.get("http://localhost/addressbook/")

    def handleAlert(self, expected_text, action):
        wd = self.wd
        try:
            WebDriverWait(wd, 3).until(EC.alert_is_present(), expected_text)
            alert = wd.switch_to.alert
            if action == 'OK':
                alert.accept()
            elif action == 'Cancel':
                alert.dismiss()
            else:
                raise Exception('Unexpected action for alert')
        except TimeoutException:
            print("No alert")


    def destroy(self):
        self.wd.quit()

    def processDateStr(self, birthdayStr):
        if birthdayStr is not None:
            bd_string = str.split(birthdayStr, '-')
            birthdayDict = {'day' : bd_string[0],
                            'month' : bd_string[1],
                            'year' : bd_string[2]}
        else:
            birthdayDict = {'day': None,
                            'month': None,
                            'year': None}
        return birthdayDict