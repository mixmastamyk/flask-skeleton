'''
    This is the common config file.
'''
import sys  #, os
from os.path import abspath, dirname, join
from datetime import timedelta

from .meta import appname, orgname, fullname

basedir = abspath(dirname(__file__))
_1MB = 1000000


# -- config values -----------------------------------------------------------

# App custom config
APP_API_PREFIX = '/api/v1'
APP_DEFAULT_ADMIN_USER = dict(name='admin', email='admin@mydomain.com',
                              password='needs one!', timezone='US/Pacific',
                              desc='Real men of genius')
APP_DEFAULT_ORG = dict(name='MyCompany, Inc.', desc='A big eastern syndicate')
APP_DEFAULT_ROLE = dict(name='end-user', desc='Run of the mill user.')
APP_FULLNAME = fullname
APP_MENU_LINKS = (
    dict(name=appname + ' Home', category='Links', url='http://..'),
    dict(name='Menu editable', category='Links', url='http://www.google.com/'),
    dict(name='in config.py', category='Links', url='http://mozilla.org/'),
)
APP_MAX_PLAYLIST_LEN = 40
APP_MIN_PASSWD_LENGTH = 8
APP_ORGNAME = orgname
APP_SECURITY_PREFIX = '/security'


UPLOAD_CHUNK_LENGTH = 8 * _1MB
UPLOADED_FILES_DEST = '/tmp'
UPLOAD_FSIZE_THRESHOLD = _1MB
UPLOAD_MAX_FILES = 20
# var below needs to render in .gs, so leave as list:
UPLOAD_UNSAVORY_EXTS = ['bat', 'cmd', 'exe', 'iso', 'php', 'vbs']


# flask and extension config
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEFAULT_TIMEZONE = 'America/Pacific'

# rest api token authentication
JWT_AUTH_HEADER_PREFIX = 'Bearer'
JWT_AUTH_URL_RULE = join(APP_SECURITY_PREFIX, 'auth')
JWT_AUTH_USERNAME_KEY = 'email'
JWT_EXPIRATION_DELTA = timedelta(seconds=5 * 60)
JWT_LEEWAY = timedelta(seconds=60)

# mail
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
MAIL_USE_SSL = True
#~ SECURITY_SEND_REGISTER_EMAIL = (False if 'FLASK_DEBUG' in os.environ else True)
SECURITY_SEND_REGISTER_EMAIL = False

MAX_CONTENT_LENGTH_MB = 10  # MB (10³), not MiB (2¹⁰)
#~ MAX_CONTENT_LENGTH_MB = 32
MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_MB * _1MB  # flask setting

SECRET_KEY = 'Yabba Dabba Dooooooo!!!'

# flask security
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = True         # needs field
SECURITY_CONFIRM_EMAIL_WITHIN = '3 days'
SECURITY_DEFAULT_REMEMBER_ME = True
SECURITY_EMAIL_SENDER = '%s Autobot <no-reply@localhost>' % fullname
SECURITY_PASSWORD_HASH = 'bcrypt'   # or 'pbkdf2_sha512' 'sha512_crypt'
SECURITY_PASSWORD_SALT = '¡Arriba, Arriba!'
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RESET_PASSWORD_WITHIN = '3 days'
SECURITY_TOKEN_MAX_AGE = 60 * 60    # seconds = 1 hour
SECURITY_TRACKABLE = True           # needs fields
SECURITY_URL_PREFIX = APP_SECURITY_PREFIX

# SQL Alchemy
#~ SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@server/dbname')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'app.db')
# now using logging and debug toolbar instead of sqla echo:
SQLALCHEMY_ECHO = False
SQLALCHEMY_MIGRATE_REPO = join(basedir, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = False


WTF_CSRF_ENABLED = True  # default, but just in case


# -- local config values -----------------------------------------------------

try:  # may overwrite vars above
    sys.path.append('..')
    from config_local import *  # noqa: F403,F401
    sys.path.pop()
except ImportError as err:
    from logcfg import log
    log.warn('local config not found: %s', err)
