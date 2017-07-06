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
# gets remote address header through proxy:
from werkzeug.contrib.fixers import ProxyFix

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
from .logcfg import log
from . import  models, forms, views, admin, utils

# security package
user_datastore = SQLAlchemyUserDatastore(db, models.Users, models.Roles)
security = Security(app, user_datastore,
                    login_form=forms.ExLoginForm,
                    confirm_register_form=forms.ExRegForm,
                    send_confirmation_form=forms.ExSendConfForm,
                    forgot_password_form=forms.ExForgotPasswordForm,
)

# flask-restless shenanigans:
from .auth import rest_preprocessors
api = APIManager(app, flask_sqlalchemy_db=db, preprocessors=rest_preprocessors)
models.register_models_with_api(api)


# modify jinja defaults, strip extra whitespace
app.jinja_options = dict(**app.jinja_options.copy(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def init_db(**kwargs):
    ''' Make sure database is ready, and there's an admin user. '''
    from datetime import datetime as dt
    from sqlalchemy.exc import IntegrityError, InvalidRequestError

    log.debug('creating tables')
    db.create_all()
    try:
        usr_config = config.APP_DEFAULT_ADMIN_USER.copy()
        usr_config.update(**kwargs)

        log.debug('creating initial records')
        o = models.Orgs(**config.APP_DEFAULT_ORG)
        r = models.Roles(**config.APP_DEFAULT_ROLE, org=o)
        u = models.Users(org=o, roles=r, admin=True, **usr_config)
        u.confirmed_at = dt.utcnow()

        db.session.add_all([r, o, u])
        db.session.commit()

    except (IntegrityError, InvalidRequestError) as err:
        log.info('starter objects created already: %s', err)
        db.session.rollback()


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
    # At startup, before-before first request.  Once with gunicorn --preload.
    init_db()


atexit.register(on_shutdown)  # still needs a signal handler
admin; views;  # shut up pyflakes
log.info('By your command…')

