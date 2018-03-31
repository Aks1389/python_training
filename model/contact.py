from sys import maxsize

class Contact:
    def __init__(self, first_name=None, last_name=None, birthday=None, address=None,
                 email=None, company=None, all_phones=None,
                 home_phone=None, mobile_phone=None, all_emails=None,
                 work_phone=None, secondary_phone=None,
                 email_1=None, email_2=None, email_3=None, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.address = address
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.work_phone = work_phone
        self.secondary_phone = secondary_phone
        self.email = email
        self.company = company
        self.all_phones = all_phones
        self.all_emails = all_emails
        self.email_1 = email_1
        self.email_2 = email_2
        self.email_3 = email_3
        self.id = id

    def __repr__(self):
        return "%s_%s:%s" % (self.last_name, self.first_name, self.id)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.first_name == other.first_name and \
               self.last_name == other.last_name

    def id_or_max(gr):
        if gr.id:
            return int(gr.id)
        else:
            return maxsize
