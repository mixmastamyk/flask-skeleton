'''
    Manually configured and automatic forms defined here.
'''
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField  #, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length
from wtforms_alchemy import model_form_factory

from flask_security.forms import (LoginForm, ConfirmRegisterForm,
                                  SendConfirmationForm, ForgotPasswordForm)

from .config import APP_MIN_PASSWD_LENGTH as MIN_LEN
from .models import Users

ModelForm = model_form_factory(FlaskForm)


# override and extend the secuity views
class ExLoginForm(LoginForm):
    email = EmailField('foo@bar.com', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(), Length(MIN_LEN)])


class ExRegForm(ConfirmRegisterForm):
    org = StringField('Name of Organization', [InputRequired(), Length(6)])
    email = EmailField('foo@bar.com', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired(), Length(MIN_LEN)])
    #~ password_confirm = # skipped due to confirmation mail.


class ExSendConfForm(SendConfirmationForm):
    submit = SubmitField('Resend Confirmation')


class ExForgotPasswordForm(ForgotPasswordForm):
    submit = SubmitField('Reset Password')


# automated forms
common_exclusions = tuple('password created_at updated_at'.split())


class UserForm(ModelForm):
    class Meta:
        model = Users
        exclude = common_exclusions
        #~ only = tuple('''
            #~ name email timezone desc
        #~ '''.split())
        only = tuple('name email timezone desc'.split())
