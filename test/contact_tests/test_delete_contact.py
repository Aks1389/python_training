
def test_delete_first_contact(app):
    app.session.login(username='admin', password='secret')
    app.contact.delete(1)
    app.session.logout()