from datetime import datetime, timezone
from flask import Flask, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import argparse
from waitress import serve


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    wishlists: Mapped[list["Wishlist"]] = relationship(
        back_populates="user"
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Wishlist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    state: Mapped[int] = mapped_column(default=0)
    items: Mapped[list["Item"]] = relationship(
       back_populates="wishlist",
       cascade="all, delete-orphan"
   )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="wishlists")

class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    updated: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    state: Mapped[int] = mapped_column(default=0)
    wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlist.id"))
    wishlist: Mapped["Wishlist"] = relationship(back_populates="items")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wishlist.db"
app.config["SECRET_KEY"] = "vanilkova zmrzlina"  # TODO: make random?
# initialize the app with the extension
db.init_app(app)


login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect to /login when user is not logged in

@login_manager.user_loader
def load_user(user_id):
   return db.session.get(User, int(user_id))

@app.route("/login", methods=['GET', 'POST'])
def login():
  pass

@app.route("/register", methods=['GET', 'POST'])
def register():
  pass

@app.route("/logout", methods=['POST'])
def logout():
  pass

@app.route("/")
def hello_world():
    return render_template("base.html", content="Hello World")

@app.route("/clicked", methods=['POST'])
def clicked():
    return "<p>clicked</p>"

@app.route("/wishlist", methods=['POST'])
@login_required
def add_list():
    return "<p>added wishlist</p>"

@app.route("/item", methods=['POST'])
@login_required
def add_item():
    return "<p>added item</p>"

@app.route("/item/reserve/<int:id>", methods=['PATCH'])
@login_required
def reserve_item(id):
    return f"<p>reserved item {id}</p>"

@app.route("/item/claim/<int:id>", methods=['PATCH'])
@login_required
def claim_item(id):
    return f"<p>claimed item {id}</p>"

@app.route("/item/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_item(id):
    return f"<p>archived item {id}</p>"

@app.route("/wishlist/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_list(id):
    return f"<p>archived wishlist {id}</p>"

@app.route("/wishlist/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_list(id):
    return f"<p>deleted wishlist {id}</p>"

@app.route("/item/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_item(id):
    return f"<p>deleted item {id}</p>"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wishlist app')
    parser.add_argument('--port', type=int, default=5000, help='Port on which the app should run')
    parser.add_argument('--prod', action='store_true', help='Run in production mode')
    args = parser.parse_args()

    with app.app_context():
        db.create_all()

    if args.prod:
        serve(app, host='0.0.0.0', port=args.port)
    else:
        # flask debug server
        app.run(debug=True, port=args.port)