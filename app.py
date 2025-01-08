from datetime import datetime, timezone
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    wishlists: Mapped[list["Wishlist"]] = relationship(
        back_populates="user"
    )

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
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def hello_world():
    return render_template("base.html", content="Hello World")

@app.route("/clicked", methods=['POST'])
def clicked():
    return "<p>clicked</p>"

@app.route("/wishlist", methods=['POST'])
def add_list():
    return "<p>added wishlist</p>"

@app.route("/item", methods=['POST'])
def add_item():
    return "<p>added item</p>"

@app.route("/item/reserve/<int:id>", methods=['PATCH'])
def reserve_item(id):
    return f"<p>reserved item {id}</p>"

@app.route("/item/claim/<int:id>", methods=['PATCH'])
def claim_item(id):
    return f"<p>claimed item {id}</p>"

@app.route("/item/archive/<int:id>", methods=['PATCH'])
def archive_item(id):
    return f"<p>archived item {id}</p>"

@app.route("/wishlist/archive/<int:id>", methods=['PATCH'])
def archive_list(id):
    return f"<p>archived wishlist {id}</p>"

@app.route("/wishlist/delete/<int:id>", methods=['DELETE'])
def delete_list(id):
    return f"<p>deleted wishlist {id}</p>"

@app.route("/item/delete/<int:id>", methods=['DELETE'])
def delete_item(id):
    return f"<p>deleted item {id}</p>"