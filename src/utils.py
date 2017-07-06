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
