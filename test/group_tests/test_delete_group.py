
def test_delete_first_group(app):
    app.group.create_if_absent()
    app.group.delete(1)