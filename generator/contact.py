from model.contact import Contact
import os.path
import jsonpickle
import getopt
import sys
import random
import string
import datetime
import re

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contacts", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = "data/contacts.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def random_phone():
    return "+"+random.choice(string.digits)+"".join([random.choice(string.digits + " "*7) for i in range(11)])

def random_date():
    date = (datetime.date.today() - datetime.timedelta(days=random.randint(0,29999))).strftime("%d-%B-%Y")
    return re.sub("^0","", date)

def random_email():
    symbols = string.ascii_letters + string.digits
    return "".join([random.choice(symbols) for i in range(random.randrange(10))])+ "@" + \
           "".join([random.choice(symbols) for i in range(random.randrange(4))]) + ".com"


testdata = [Contact(first_name="", last_name="")] + [
    Contact(first_name=random_string("name", 7), last_name=random_string("", 12), birthday=random_date(),
            address=random_string("street ", 15), mobile_phone=random_phone(), email=random_email(),
            company=random_string("comp.", 10))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))