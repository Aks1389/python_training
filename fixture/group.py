from model.group import Group

class GroupHelper:
    group_cache = None

    def __init__(self, app):
        self.app = app

    def return_to_groups_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("group page").click()

    def create(self, group):
        wd = self.app.wd

        wd.find_element_by_name("new").click()
        wd.find_element_by_name("group_name").click()
        self.fill_fields(group)
        # submit group creating
        wd.find_element_by_name("submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def update(self, index, group):
        wd = self.app.wd
        self.open_groups_page()

        #updating
        self.select_group_by_index(index)
        wd.find_element_by_xpath("//input[@name = 'edit']").click()
        self.fill_fields(group)
        wd.find_element_by_xpath("//input[@name = 'update']").click()
        self.return_to_groups_page()
        self.group_cache = None


    def select_group_by_index(self, index):
        wd = self.app.wd
        groups_list = wd.find_elements_by_xpath("//input[@type = 'checkbox']")
        assert (len(groups_list) >= index), "Number of groups is less than index"
        groups_list[index-1].click()

    def fill_fields(self, group):
        # fill group form
        wd = self.app.wd
        self.set_field_value("group_name", group.name)
        self.set_field_value("group_header", group.header)
        self.set_field_value("group_footer", group.footer)

    def set_field_value(self, field_name, field_obj):
        wd = self.app.wd
        if field_obj is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(field_obj)

    def delete(self, index):
        wd = self.app.wd
        self.select_group_by_index(index)
        wd.find_element_by_xpath("//input[@value = 'Delete group(s)']").click()
        self.return_to_groups_page()
        self.group_cache = None

    def open_groups_page(self):
        # open groups page
        wd = self.app.wd
        if not (wd.current_url.endswith("group.php") and len(wd.find_elements_by_xpath("//input[@value = 'New group']"))>0):
            wd.find_element_by_link_text("groups").click()

    def get_groups_number(self):
        wd = self.app.wd
        number = len(wd.find_elements_by_xpath("//span[@class = 'group']"))
        print("Number of groups: " + str(number))
        return number

    def create_if_absent(self):
        self.open_groups_page()
        if self.get_groups_number() == 0:
            self.create(Group(name="testGroup"))
            self.open_groups_page()

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.open_groups_page()
            self.group_cache = []
            for element in wd.find_elements_by_xpath("//span[@class = 'group']"):
                text = element.text
                id = element.find_element_by_xpath(".//input[@type='checkbox']").get_attribute("value")
                self.group_cache.append(Group(name=text, id=id))
            print("Groups list: " + str(self.group_cache))
        return list(self.group_cache)