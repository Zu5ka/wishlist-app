"""Create a wishlist app that allows users to create, edit and share wishlists and reserve items."""

import secrets
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# third-party library
# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """Required by SQLAlchemy."""

db = SQLAlchemy(model_class=Base)
DEFAULT_DB = "sqlite:///wishlist.db"

# the database needs to be initialised before import
# pylint: disable=wrong-import-position
from . import models

# the database needs to be initialised before import
# pylint: disable=wrong-import-position
from .models import ItemState, ListState

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Load current user.

    required for login_manager
    """
    return db.session.get(models.User, int(user_id))

def create_app(db_url=None, secret=None):
    """Create a wishlist app that allows users to create, edit and share wishlists and reserve items."""
    wishlist_app = Flask(__name__)
    wishlist_app.config["SQLALCHEMY_DATABASE_URI"] = db_url or DEFAULT_DB
    wishlist_app.config["SECRET_KEY"] = secret or secrets.token_hex(32)
    wishlist_app.jinja_env.globals["ItemState"] = ItemState
    wishlist_app.jinja_env.globals["ListState"] = ListState

    db.init_app(wishlist_app)
    login_manager.init_app(wishlist_app)
    login_manager.login_view = (
        "auth.login"  # redirect to /login when user is not logged in
    )

    # the import has to be there
    # pylint: disable=import-outside-toplevel
    from .auth import auth_blueprint
    # the import has to be there
    # pylint: disable=import-outside-toplevel
    from .views import views_blueprint

    wishlist_app.register_blueprint(auth_blueprint)
    wishlist_app.register_blueprint(views_blueprint)

    return wishlist_app
