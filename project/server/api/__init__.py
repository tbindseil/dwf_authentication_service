from flask import Blueprint

from .register import RegisterAPI
from .login import LoginAPI
from .user import UserAPI
from .logout import LogoutAPI

# create blueprints
auth_blueprint = Blueprint('auth', __name__)
login_blueprint = Blueprint('login', __name__)
user_blueprint = Blueprint('user', __name__)
logout_blueprint = Blueprint('logout', __name__)

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
login_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/auth/user',
    view_func=user_view,
    methods=['GET']
)
logout_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
