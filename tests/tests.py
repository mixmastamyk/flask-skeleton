# http://flask.pocoo.org/docs/latest/testing/

import sys, os
import unittest
import tempfile

# make app available:
sys.path.insert(0, os.path.abspath('../main'))
import main
from main import app

username = 'admin@mydomain.com'
password = 'needs one!'


class TestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            main.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/security/login', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/security/logout', follow_redirects=True)

    def test_first_user(self):          # doesn't work, CSRF token missing?
        rv = self.login(username, password)
        rv = self.app.get('/users/1')
        assert b'admin@' in rv.data

    def test_login_logout(self):
        rv = self.login(username, password)
        assert b'Hello World' in rv.data

        rv = self.logout()
        assert b'You were logged out' in rv.data

        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data

        rv = self.login(username, 'defaultx')
        assert b'Invalid password' in rv.data

    def test_messages(self):  # doesn't work
        rv = self.login(username, password)
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()

