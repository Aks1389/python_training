
def test_delete_first_contact(app):
    app.contact.create_if_absent()
    app.contact.delete(1)