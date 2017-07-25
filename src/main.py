'''
    Main startup file.
'''
import atexit
import logging

from flask import Flask
from flask_admin import Admin
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restless import APIManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix  # use remote address header

from . import config
from .meta import fullname


# main objects
app = Flask(__name__)
app.config.from_object(config)
app.wsgi_app = ProxyFix(app.wsgi_app)  # remote address header fix
admin = Admin(app, name=fullname, template_mode='bootstrap3')
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)


# additional imports below to avoid circular import issues with app, db, etc.
from .logcfg import log  # noqa: E402
from . import models, forms, views, admin, utils, errors  # noqa: F401,E402
try:
    import models_app  # application models
except ImportError:
    models_app = None

# security package
user_datastore = SQLAlchemyUserDatastore(db, models.Users, models.Roles)
security = Security(app, user_datastore,
                    login_form=forms.ExLoginForm,
                    confirm_register_form=forms.ExRegForm,
                    send_confirmation_form=forms.ExSendConfForm,
                    forgot_password_form=forms.ExForgotPasswordForm,
                   )

# flask-restless shenanigans:
from .auth import rest_preprocessors  # noqa: E402
api = APIManager(app, flask_sqlalchemy_db=db, preprocessors=rest_preprocessors)
models.register_models_with_api(models, api)
if models_app:
    models.register_models_with_api(models_app, api)


def on_shutdown():
    ''' Tasks to do on shutdown, such as cleanup should be added here. '''
    print()  # newline on ^C
    log.info('Moriturus te saluto.')
    logging.shutdown()


if app.debug:
    # only load toolbar when in debug mode
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)
else:
    # At startup, before before-first request.  Once with gunicorn --preload.
    models.initdb()


# modify jinja defaults, strip extra whitespace
app.jinja_options = dict(**app.jinja_options.copy(),
                         trim_blocks=True,
                         lstrip_blocks=True,
                        )

atexit.register(on_shutdown)    # still needs a signal handler
log.info('By your command…')
