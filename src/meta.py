'''
    Project metadata is specified here.

    This module *should not* import anything from the project or third-party
    modules, to avoid dependencies in setup.py or circular import issues.
'''
from time import localtime as _localtime


orgname         = 'Flask'
appname         = 'App++'
appname_low     = appname.lower().rstrip('+')  # rm rstrip on name change
fullname        = '%s %s' % (orgname, appname)
# reversed dotted notation, for libraries, android, etc:
revname         = '.'.join(reversed(orgname.split('.'))) + '.' + appname

__version__     = version = '0.50'
__author__      = authors = ', '.join([
                                'Firstinald_M_McLasterson',  # add more below
                                'and contributors',
                            ])
copyright_date  = '© 2017-%s' % _localtime().tm_year
__copyright__   = copyright = '%s, %s' % (copyright_date, orgname)

description     = 'A_short_descriptive_blurb_to_explain_the_project_goes_here.'
# delete this line and line below when description has been updated:
description    += ''' (Edit title, version, and this description, etc. in
                      ../main/meta.py) '''
email           = 'foo@bar.com',

#~ __license__     = license = 'Proprietary, see LICENSE file for details.'
__license__     = license = 'Unlicense, The - https://unlicense.org'

pkg_reqs        = (  # for setup.py
    'bcrypt',
    'flask>=0.12',
    'flask_admin',
    'flask_debugtoolbar',
    'flask_jwt',
    'flask_migrate',
    'flask_restless>=0.20',
    'flask_security',
    'flask_sqlalchemy',
    'flask_wtf',
    'http_status',
    'pytz',
    'sqlalchemy_utils',
    'wtforms_alchemy',
)
pkg_docs_reqs = (
    'sphinx',
    'sphinx_rtd_theme',
    'sphinx_fontawesome',
)

# online repo information
repo_account    = 'ACCOUNT_NAME'
repo_name       = 'REPO_NAME'
repo_provider   = 'github.com'
#~ repo_provider   = 'bitbucket.org'
repo_url        = 'https://%s/%s/%s' % (repo_provider, repo_account, repo_name),


class defaults:
    name        = 'foo'


def print_env(prefix=''):
    ''' Print metadata as environment vars, for sourcing in shell scripts. '''
    # filter for "public" strings
    var_list = [ (key, val) for key, val in globals().items()
                            if not key.startswith('_')
                            if type(val) is str ]

    for key, val in sorted(var_list):
        key = key.upper()
        if key.startswith(prefix):  # appname var makes this redundant :-/
            key = key.strip(prefix)
        print('{}_{}={!r}'.format(prefix, key, val))
