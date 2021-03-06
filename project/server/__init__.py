import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.api import auth_blueprint, login_blueprint, user_blueprint, logout_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(logout_blueprint)
