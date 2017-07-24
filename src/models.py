'''
    Not the swimsuit edition - additional application models.
'''
from sqlalchemy import (
    #~ Boolean,
    Column,
    #~ DateTime,
    #~ ForeignKey,
    #~ Integer,
    #~ String,
    #~ Table,
    #~ Text,
)
from sqlalchemy_utils import ChoiceType  # TimezoneType

from .main import db
from .database import MultiTenantBase


#~ class BaseMixin:
    #~ ''' This parent model mixin contains common fields. '''
    #~ id = Column(Integer, index=True, unique=True, primary_key=True)
    #~ name = Column(String(127), index=True, nullable=False)
    #~ desc = Column(Text(255), default='')
    #~ # now() updated to current_timestamp:
    #~ # https://groups.google.com/forum/#!topic/sqlalchemy/7A6LCOKnrVY
    #~ created_at = Column(DateTime, server_default=db.func.current_timestamp())
    #~ updated_at = Column(DateTime, server_default=db.func.current_timestamp(),
                                #~ server_onupdate=db.func.current_timestamp())

# Add application models below
#~ class Thing(MultiTenantBase, db.Model):
    #~ ''' Descriptive_text_goes_here. '''
    #~ pass
