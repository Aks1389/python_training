
def test_delete_first_contact(app):
    app.hm.session.login(username='admin', password='secret')
    app.hm.contact.delete(1)
    app.hm.session.logout()