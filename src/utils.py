from os.path import exists, join

from flask.json import JSONEncoder
from ipaddress import _BaseAddress
from pytz.tzinfo import DstTzInfo

from .main import app
from .logcfg import log


class CustomJSONEncoder(JSONEncoder):
    ''' Handles odd datatypes. '''
    def default(self, obj):
        if isinstance(obj, (_BaseAddress, DstTzInfo)):
            return str(obj)
        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


class ansi:
    ''' Colored text in logs. '''
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    GREEN = '\033[92m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

    BOLD = '\033[1m'
    END = '\033[0m'
    UNDERLINE = '\033[4m'


def get_status_category(status_code):
    ''' Returns the category from a given HTTP status code. '''
    if 100 <= status_code < 200:
        cat = 'informational'
    elif 200 <= status_code < 300:
        cat = 'success'
    elif 300 <= status_code < 400:
        cat = 'redirection'
    elif 400 <= status_code < 500:
        cat = 'client error'
    elif 500 <= status_code < 600:
        cat = 'server error'
    else:
        cat = 'invalid'

    return cat


def first_of(*paths, root='src/templates'):
    ''' return first existing path. '''
    for path in paths:
        test_path = join(root, path)
        log.debug('looking for template at: %r', test_path)
        if exists(test_path):
            return path
