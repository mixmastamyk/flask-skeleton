'''
    Configure the Administration app.
'''
import logging;  log = logging.getLogger(__name__)  # fix

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin.form.fields import Select2Field
from flask_login import current_user
from wtforms.fields import PasswordField
#~ from wtforms.validators import Length

from .main import admin, db
from .models import Orgs, Roles, Users
#~ from .config import APP_MIN_PASSWD_LENGTH as MIN_LEN
from .timezones import all_tz


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


class UserView(AdminModelView):
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


class OrgView(AdminModelView):
    column_list = ('name', 'updated_at', 'desc')    # order
    form_rules = ('name', 'users', 'desc')


class RoleView(AdminModelView):
    form_rules = ('name', 'users', 'org', 'desc')


log.info('adding admin views.')
admin.add_view(OrgView(Orgs, db.session))
admin.add_view(RoleView(Roles, db.session))
admin.add_view(UserView(Users, db.session))
