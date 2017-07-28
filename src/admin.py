'''
    Configure the Administration app.
'''
import sys

from flask_admin.base import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin.form.fields import Select2Field
from flask_login import current_user
from wtforms.fields import PasswordField
#~ from wtforms.validators import Length

from .logcfg import log
from .main import db
from .models import Orgs, Roles, Users  # noqa: F401  # they are used
#~ from .config import APP_MIN_PASSWD_LENGTH as MIN_LEN
from .timezones import all_tz


# admin home page view
class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        from .main import adm
        return self.render('admin/index.html', views=adm._views,
                           hasattr=hasattr)


class AdminModelView(ModelView):
    ''' Customize admin default behavior. '''
    page_size = 50                  # num entries to display on the list view
    can_export = True
    can_view_details = True
    column_editable_list = ('desc',)
    column_display_pk = True
    column_exclude_list = (
        'confirmed_at',
        'created_at',
        'current_login_at',
        'current_login_ip',
        'id',
        'last_login_at',
        'last_login_ip',
        'password',
    )
    column_labels = dict(desc='Description')            # full word for display
    column_list = ('name', 'org', 'updated_at', 'desc')    # order
    column_searchable_list = ('name', 'desc')
    form_base_class = SecureForm
    form_excluded_columns = (
        'created_at',
        'last_login_at'
        'last_login_ip',
        'updated_at',
    )
    form_widget_args = {
        'confirmed_at': {'readonly': True},
        'created_at': {'readonly': True},
        'current_login_at': {'readonly': True},
        'current_login_ip': {'readonly': True},
        'desc': { 'rows': 3, 'maxlength': '255'},
        'last_login_at': {'readonly': True},
        'last_login_ip': {'readonly': True},
        'login_count': {'readonly': True},
        'updated_at': {'readonly': True},
        'password': {'readonly': True},
    }

    def is_accessible(self):
        ''' Prevent administration of models unless an admin. '''
        return current_user.admin

    #~ def on_model_change(self, form, model, is_created):
        #~ ''' Common tasks handled here. '''


class UsersAdmin(AdminModelView):
    icon = dict(gi='user', fa='user')
    column_labels = dict(name='Nick')
    column_filters = ('org.name',)
    column_list = ('name', 'email', 'active', 'admin', 'updated_at',
                   'login_count', 'desc')  # order
    column_searchable_list = ('name', 'email', 'desc')
    form_create_rules = ('admin', 'email', 'name', 'password2', 'org', 'roles',
                         'timezone2', 'desc')
    form_edit_rules   = form_create_rules + ('confirmed_at',)

    # Special password handling:
    # https://github.com/sasaporta/flask-security-admin-example/blob/master/main.py
    # First, we want to encrypt the password before storing in the database.
    # Second, we want to use a password field (with the input masked) rather
    # than a regular text field.
    form_extra_fields = {
        'password2': PasswordField('New Password',),  # [Length(MIN_LEN)]
        'timezone2': Select2Field('Timezone (write only)', choices=all_tz, ),
    }

    def on_form_prefill(self, form, id):  # doesn't work
        #~ form.timezone2.data = 'US/Mountain'
        #~ form.timezone2.process_data(3)
        #~ form.timezone2.process_data('US/Mountain')
        pass

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)

        data = form.password2.data
        log.warn('data: %r', data)  # ?
        if data != '':
            model.set_password(data)
        data = form.timezone2.data
        if data != '':
            model.timezone = data


class OrgsAdmin(AdminModelView):
    icon = dict(gi='briefcase', fa='group')
    column_list = ('name', 'updated_at', 'desc')    # order
    form_rules = ('name', 'users', 'desc')


class RolesAdmin(AdminModelView):
    icon = dict(gi='briefcase', fa='briefcase')
    form_rules = ('name', 'users', 'org', 'desc')


def register_models_with_admin(model_module,
                               admin_module=sys.modules[__name__]):
    ''' Add all models to the admin site automatically. '''
    import inspect
    from .main import adm
    log.info('adding admin views.')

    for name, class_ in inspect.getmembers(model_module, inspect.isclass):
        if issubclass(class_, db.Model):
            log.debug('adding %s', class_.__name__)
            try:
                admin_class = getattr(admin_module, class_.__name__ + 'Admin')
            except AttributeError as err:
                log.error('Admin class not found: %s', err)
            else:
                adm.add_view(admin_class(class_, db.session))


def configure_menu_links(adm):
    ''' Add links to the admin menu bar. '''
    from flask_admin.menu import MenuLink
    from .config import APP_MENU_LINKS

    for link_args in APP_MENU_LINKS:
        adm.add_link(MenuLink(**link_args))
