import pymysql.cursors
from model.group import Group
from model.contact import Contact
import re

class DbFixture:

    def __init__(self, host, name, user, password):
        self.host=host
        self.name=name
        self.user=user,
        self.password=password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password)
        self.connection.autocommit(True)

    def destroy(self):
        self.connection.close()


    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, firstname, lastname from addressbook where deprecated = '0000-00-00 00:00:00'")
            for row in cursor:
                (id, first_name, last_name) = row
                list.append(Contact(id=str(id), first_name=first_name, last_name=last_name))
        finally:
            cursor.close()
        return list

    def get_full_contacts_info(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("""SELECT id, firstname, lastname, address,
		                            concat(IF(email='', '', email), 
                                           IF(email2='', '', concat('\\n', email2)),
                                           IF(email3='', '', concat('\\n', email3))) as 'emails',
                                    concat(IF(home='', '', home), 
                                           IF(mobile='', '', concat('\\n', mobile)),
                                           IF(work='', '', concat('\\n', work))) as 'phones' 
                              FROM addressbook WHERE deprecated = '0000-00-00 00:00:00'""")
            for row in cursor:
                (id, first_name, last_name, address, emails, phones) = row
                list.append(Contact(id=str(id), first_name=self.format_str(first_name), last_name=self.format_str(last_name),
                                    address=address.strip(), all_emails=emails.strip(), all_phones=phones.strip()))
        finally:
            cursor.close()
        return list

    def format_str(self, string):
        return re.sub("\s{2,}", " ", string.strip())