'''
    Error handlers are defined here
'''
import werkzeug.exceptions

from .main import app
#~ from .logcfg import log


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(err):
    return 'Bad Request!  (Change in errors.py)'


if not app.debug:

    @app.errorhandler(Exception)
    def handle_exception(err):
        msg = 'Err handler: Exception occurred: %s' % err
        return msg
