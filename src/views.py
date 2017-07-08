'''
    Controllers/views for the web interface are defined here.
'''
from flask import (
    flash,      # flash categories: success, (blank) info, warning, error
    redirect,
    render_template as render,
    request,
    #~ session,
    url_for
)
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from .main import app, db
from .database import Users
from .meta import fullname
from .logcfg import log
from .forms import UserForm


SKIP_LOGIN =  ('static', '_default_auth_request_handler')
app_debug = app.debug
sec_bp = app.config.get('SECURITY_BLUEPRINT_NAME', 'security')


@app.before_request
def before_request():
    ''' Every request should be logged-in, thanks. '''
    endpoint = request.endpoint
    if app_debug:
        if endpoint not in ('static', 'admin.static', '_debug_toolbar.static'):
            log.note('endpoint: %s  user: %s  auth: %s  bp: %s', endpoint,
                     hasattr(current_user, 'email') and current_user.email,
                     current_user.is_authenticated, request.blueprint)

    if not current_user.is_authenticated and endpoint:  # sometimes None
        if ((endpoint not in SKIP_LOGIN) and
            (not request.blueprint == sec_bp) and
            (not endpoint.endswith('api')) ):
                return redirect(url_for('security.login', next=request.path))


# simple example views
@app.route('/')
def index():
    return render('index.html', title='Home', fullname=fullname)


@app.route('/routes')
def routes():
    rules = list(app.url_map.iter_rules())
    rules.sort(key=lambda r: r.rule)

    return render('routes.html', title='Routes configured',
                  fullname=fullname, routes=rules)


@app.route('/users/<int:uid>', methods=('GET', 'POST'))
def show_user(uid):
    # get user and form
    user = Users.query.filter_by(id=uid).first_or_404()
    form = UserForm(obj=user)
    # http://wtforms-alchemy.readthedocs.io/en/latest/validators.html#using-unique-validator-with-existing-objects
    form.populate_obj(user)     # handle update + unique constraints

    if request.method == 'POST':
        try:
            form.validate()
            for field in form:
                setattr(user, field.short_name, field.data)
            db.session.commit()
            flash('User updated.', 'success')
        except SQLAlchemyError as err:
            log.error(str(err))
            db.session.rollback()
            flash('Database: %s' % err.orig, 'error')

        return redirect(url_for('show_user', uid=uid))

    return render('user.html', title='User Page', fullname=fullname, form=form)

