'''
    Error handlers are defined here
'''
import werkzeug.exceptions

from .main import app
from .logcfg import log


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(err):
    return 'Bad Request!  (Change in errors.py)'


@app.errorhandler(Exception)
def handle_exception(err):
    'needs traceback?'
    #~ msg = 'Err handler: Exception occurred: %s' % err
    msg = 'Err handler: Exception occurred:'
    #~ log.error(msg)
    log.exception(msg)
    return msg
