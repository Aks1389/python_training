
def test_delete_first_group(app):
    app.hm.session.login(username='admin', password='secret')
    app.hm.group.delete_first_group()
    app.hm.session.logout()