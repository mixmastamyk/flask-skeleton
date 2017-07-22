'''
    Authentication stuff for the REST API.
'''
from flask_security.utils import verify_password
from flask_jwt import JWT, jwt_required

from .main import app, user_datastore


def auth_handler(username, password):
    user = user_datastore.find_user(email=username)
    if username == user.email and verify_password(password, user.password):
        return user


def load_user(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user


@jwt_required()
def check_auth(*args, **kwargs):
    return True  # decorator does all the work ;-)


jwt = JWT(app, auth_handler, load_user)


# flask-restless shenanigans:
# https://flask-restless.readthedocs.io/en/latest/processors.html
keys = [
    'DELETE_RELATIONSHIP',
    'DELETE_RESOURCE',
    'GET_COLLECTION',
    'GET_RELATED_RESOURCE',
    'GET_RELATION',
    'GET_RELATIONSHIP',
    'GET_RESOURCE',
    'PATCH_RELATIONSHIP'
    'PATCH_RESOURCE',
    'POST_RELATIONSHIP',
    'POST_RESOURCE',
]
validators = [check_auth]

# configure all for authentication
rest_preprocessors = { key: validators for key in keys }
