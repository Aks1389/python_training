from fixture.session import SessionHelper
from fixture.group import GroupHelper
from fixture.contact import ContactHelper

class HelpersManager:
    def __init__(self, app):
        self.session = SessionHelper(app)
        self.group = GroupHelper(app)
        self.contact = ContactHelper(app)