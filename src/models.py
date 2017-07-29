'''
    Core database models and tools are contained here.
'''
from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password, verify_password
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import IPAddressType, TimezoneType

from . import config
from .main import app, db
from .logcfg import log


class BaseMixin:
    ''' This parent model mixin contains common fields. '''
    id = Column(Integer, index=True, unique=True, primary_key=True)
    name = Column(String(127), index=True, nullable=False)
    desc = Column(Text(255), default='')
    # now() updated to current_timestamp:
    # https://groups.google.com/forum/#!topic/sqlalchemy/7A6LCOKnrVY
    created_at = Column(DateTime, server_default=db.func.current_timestamp())
    updated_at = Column(DateTime, server_default=db.func.current_timestamp(),
                                  server_onupdate=db.func.current_timestamp())
    deleted = Column(Boolean, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)

    def __str__(self):
        return str(self.name)


class MultiTenantBase(BaseMixin):
    ''' Common fields and relationships are declared here. '''

    @declared_attr
    def org_id(cls):
        return Column(Integer, ForeignKey('orgs.id'), nullable=False)

    @declared_attr
    def org(cls):
        return db.relationship('Orgs')


class Orgs(BaseMixin, db.Model):
    ''' Organization, aka multi-tenant model. '''
    # don't want duplicate names in this table:
    name = Column(String(64), index=True, nullable=False, unique=True)
    users = db.relationship('Users', lazy='dynamic')

    def __init__(self, name, desc=''):  # needs to have defaults for admin
        self.name = name
        self.desc = desc


class Roles(MultiTenantBase, RoleMixin, db.Model):
    name = Column(String(64), nullable=False, unique=True)  # don't want dups

    def __init__(self, name='', org=None, desc=''):
        self.name = name
        self.org = org
        self.desc = desc


# create M2M table for flask_security
roles_users = Table('roles_users', db.Model.metadata,
                    Column('user_id', Integer(), ForeignKey('users.id')),
                    Column('role_id', Integer(), ForeignKey('roles.id')),
)


class Users(MultiTenantBase, UserMixin, db.Model):
    name = Column(String(127), nullable=True)               # optional
    active = Column(Boolean, nullable=False, default=True)  # req security
    admin = Column(Boolean, nullable=False, default=False)
    email = Column(String(64), index=True, unique=True, nullable=False)
    password = Column(String(72), nullable=False)  # bcrypt.length = 60
    timezone = Column(TimezoneType(backend='pytz'))

    confirmed_at = Column(DateTime)
    last_login_at = Column(DateTime)
    current_login_at = Column(DateTime)
    login_count = Column(Integer, default=0)
    last_login_ip = Column(IPAddressType)
    current_login_ip = Column(IPAddressType)

    roles = db.relationship('Roles', secondary=roles_users,
                            backref='users', lazy='dynamic')

    def __init__(self, name='', email='', desc='', password=None,
                 active=True, admin=False, org=None, roles=None, timezone=None):
        self.active = active
        self.admin = admin
        self.desc = desc
        self.email = email
        self.name = name
        self.timezone = timezone

        if password:
            self.set_password(password)
        if roles is not None:
            if type(roles) is not list:
                roles = [roles]
            self.roles = roles

        if type(org) is str:
            orgobj = Orgs.query.filter_by(name=org).first()
            if orgobj:
                org = orgobj
            else:
                org = Orgs(name=org)
                db.session.add(org)
                db.session.commit()
        self.org = org

    def set_password(self, password):
        try:
            self.password = encrypt_password(password)
        except RuntimeError:  # :-/
            with app.app_context():
                self.password = encrypt_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.email)


def initdb_impl(**kwargs):
    ''' Make sure database is ready, and there's an admin user. '''
    from datetime import datetime as dt
    from sqlalchemy.exc import IntegrityError, InvalidRequestError

    log.debug('creating tables')
    db.create_all()
    try:
        usr_config = config.APP_DEFAULT_ADMIN_USER.copy()
        usr_config.update(**kwargs)

        log.debug('creating initial records')
        o = Orgs(**config.APP_DEFAULT_ORG)
        r = Roles(**config.APP_DEFAULT_ROLE, org=o)
        u = Users(org=o, roles=r, admin=True, **usr_config)
        u.confirmed_at = dt.utcnow()

        db.session.add_all([r, o, u])
        db.session.commit()

    except (IntegrityError, InvalidRequestError) as err:
        log.warning('starter objects created already? %s', err)
        db.session.rollback()


# click is interfering with unit tests :-/
@app.cli.command()
def initdb(**kwargs):
    initdb_impl(**kwargs)


def register_models_with_api(module, api):
    ''' Add all Model classes to the Rest API. '''
    import inspect

    default_methods = [
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
    ]
    for name, class_ in inspect.getmembers(module, inspect.isclass):
        if issubclass(class_, db.Model):
            log.debug('adding %s', class_.__name__)
            api.create_api(class_, methods=default_methods,
                           url_prefix=config.APP_API_PREFIX)
