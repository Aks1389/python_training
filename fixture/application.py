from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import WebDriver
from fixture.helpers_manager import HelpersManager

class Application:
    def __init__(self):
        self.wd = WebDriver(capabilities={"marionette": False})
        self.wd.implicitly_wait(20)
        self.hm = HelpersManager(self)
        """hm = HelpersManager(self)
        self.session = hm.session
        self.contact = hm.contact
        self.group = hm.group"""

    def go_to_main_page(self, byLink):
        wd = self.wd
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
        bd_string = str.split(birthdayStr, '-')
        birthdayDict = {'day' : bd_string[0],
                        'month' : bd_string[1],
                        'year' : bd_string[2]}
        return birthdayDict