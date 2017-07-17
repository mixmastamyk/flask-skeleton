from flask.json import JSONEncoder
from ipaddress import _BaseAddress
from pytz.tzinfo import DstTzInfo

from .main import app


class CustomJSONEncoder(JSONEncoder):
    ''' Handles odd datatypes. '''
    def default(self, obj):
        if isinstance(obj, (_BaseAddress, DstTzInfo)):
            return str(obj)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


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
