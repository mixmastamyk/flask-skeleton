'''
    Local configuration goes here
'''
import os

from src.meta import appname


APP_DEFAULT_ADMIN_USER = dict(
                            email='admin@iris.digital',
                            desc='Real men of genius.',
                            name='fred',
                            password='needs one!',
                            timezone='US/Pacific',
)
APP_DEFAULT_ROLE = dict(name='VIP', desc='Very Impatient Person')
APP_DEFAULT_ORG = dict(name='BES, Inc.', desc='A big eastern syndicate')
APP_MENU_LINKS = (
    dict(name=appname + ' Home', category='Links', url='http://..'),
    dict(name='Google', category='Links', url='http://www.google.com/'),
    dict(name='Mozilla', category='Links', url='http://mozilla.org/'),
)


MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_USE_SSL = True
SECURITY_SEND_REGISTER_EMAIL = (False if 'FLASK_DEBUG' in os.environ else True)

SECRET_KEY = 'Yabba Dabba Dooooooo!!! @#$%^&*'
