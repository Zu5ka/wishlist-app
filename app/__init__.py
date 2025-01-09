from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wishlist.db"
    app.config["SECRET_KEY"] = "vanilkova zmrzlina"  # TODO: make random?

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # redirect to /login when user is not logged in

    from . import views, auth, models

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    return app

app = create_app()