from fixture.orm import ORMFixture
import pymysql.cursors

db = ORMFixture(host="127.0.0.1", name="addressbook", user="root", password="")

try:
    items = db.get_group_list()
    for item in items:
        print(item)
    print(len(items))
finally:
    pass