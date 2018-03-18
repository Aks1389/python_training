
def test_delete_first_group(app):
    app.session.login(username='admin', password='secret')
    app.group.delete(1)
    app.session.logout()