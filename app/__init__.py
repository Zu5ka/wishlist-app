from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
from . import models
from .models import ItemState, ListState

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wishlist.db"
    app.config["SECRET_KEY"] = "vanilkova zmrzlina"  # TODO: make random?
    app.jinja_env.globals["ItemState"] = ItemState
    app.jinja_env.globals["ListState"] = ListState

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = (
        "auth.login"  # redirect to /login when user is not logged in
    )

    from .auth import auth_blueprint
    from .views import views_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(views_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    return app


app = create_app()
