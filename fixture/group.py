class GroupHelper:
    def __init__(self, app):
        self.app = app

    def return_to_groups_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("group page").click()

    def create(self, group):
        wd = self.app.wd
        self.open_groups_page()
        wd.find_element_by_name("new").click()
        wd.find_element_by_name("group_name").click()
        self.fill_fields(group)
        # submit group creating
        wd.find_element_by_name("submit").click()

    def update(self, index, group):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_index(index)
        wd.find_element_by_xpath("//input[@name = 'edit']").click()
        self.fill_fields(group)
        wd.find_element_by_xpath("//input[@name = 'update']").click()

    def select_group_by_index(self, index):
        wd = self.app.wd
        groups_list = wd.find_elements_by_xpath("//input[@type = 'checkbox']")
        assert (len(groups_list) >= index)
        groups_list[index-1].click()

    def fill_fields(self, group):
        # fill group form
        wd = self.app.wd
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys(group.name)
        wd.find_element_by_name("group_header").click()
        wd.find_element_by_name("group_header").clear()
        wd.find_element_by_name("group_header").send_keys(group.header)
        wd.find_element_by_name("group_footer").click()
        wd.find_element_by_name("group_footer").clear()
        wd.find_element_by_name("group_footer").send_keys(group.footer)

    def delete_first_group(self):
        wd = self.app.wd
        self.open_groups_page()
        groups_before_del = self.get_groups_number()
        wd.find_element_by_name("selected[]").click()
        wd.find_element_by_xpath("//input[@value = 'Delete group(s)']").click()
        self.open_groups_page()
        assert self.get_groups_number() == groups_before_del-1


    def open_groups_page(self):
        # open groups page
        wd = self.app.wd
        wd.find_element_by_link_text("groups").click()

    def get_groups_number(self):
        wd = self.app.wd
        number = len(wd.find_elements_by_xpath("//span[@class = 'group']"))
        print("Number of groups: " + str(number))
        return number