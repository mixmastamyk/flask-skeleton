# http://flask.pocoo.org/docs/latest/testing/

import os
import unittest
import tempfile

from src.main import app, models
from src.config import APP_DEFAULT_ADMIN_USER


username = APP_DEFAULT_ADMIN_USER['email']
password = APP_DEFAULT_ADMIN_USER['password']


class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_path
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            models.initdb_impl()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def login(self, username, password):
        return self.app.post('/security/login', data=dict(
            email=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/security/logout', follow_redirects=True)

    # tests begin
    def test_first_user(self):
        rv = self.login(username, password)
        rv = self.app.get('/profile')
        assert username.encode('utf8') in rv.data

    def test_login_logout(self):
        rv = self.login(username, password)
        assert b'Hello World' in rv.data

        rv = self.logout()
        assert b'Right This Way' in rv.data

        rv = self.login('adminx', 'default_pass')
        assert b'Invalid email address.' in rv.data

        rv = self.login(username, 'defaultx')
        assert b'Invalid password' in rv.data

    def test_messages(self):  # example - doesn't apply to this app
        #~ rv = self.login(username, password)
        #~ rv = self.app.post('/add', data=dict(
            #~ title='<Hello>',
            #~ text='<strong>HTML</strong> allowed here',
        #~ ), follow_redirects=True)
        #~ assert b'No entries here so far' not in rv.data
        #~ assert b'&lt;Hello&gt;' in rv.data
        #~ assert b'<strong>HTML</strong> allowed here' in rv.data
        pass


if __name__ == '__main__':
    unittest.main()
