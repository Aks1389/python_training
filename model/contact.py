from sys import maxsize

class Contact:
    def __init__(self, first_name=None, last_name=None, birthday=None, address=None,
                 phone=None, email=None, company=None, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.address = address
        self.phone = phone
        self.email = email
        self.company = company
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