from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from enum import IntEnum
from . import db

class ItemState(IntEnum):
   active = 0
   reserved = 1
   claimed = 2
   deleted = 3

class ListState(IntEnum):
   active = 0
   archived = 1
   deleted = 2

wishlist_shares = db.Table('wishlist_shares',
                           db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlist.id'), primary_key=True),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(UserMixin, db.Model):
   id: Mapped[int] = mapped_column(primary_key=True)
   username: Mapped[str] = mapped_column(unique=True)
   password_hash: Mapped[str] = mapped_column()
   wishlists: Mapped[list["Wishlist"]] = relationship(
       back_populates="user"
   )

   shared_with_me: Mapped[list["Wishlist"]] = relationship(
      secondary=wishlist_shares,
      back_populates="shared_with"
   )

   def set_password(self, password: str):
       self.password_hash = generate_password_hash(password)

   def check_password(self, password: str) -> bool:
       return check_password_hash(self.password_hash, password)

class Wishlist(db.Model):
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str] = mapped_column()
   state: Mapped[int] = mapped_column(default=ListState.active)
   items: Mapped[list["Item"]] = relationship(
      back_populates="wishlist",
      cascade="all, delete-orphan"
   )
   user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
   user: Mapped["User"] = relationship(back_populates="wishlists")

   shared_with: Mapped[list["User"]] = relationship(
      secondary=wishlist_shares,
      back_populates="shared_with_me"
   )

class Item(db.Model):
   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str] = mapped_column()
   updated: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
   state: Mapped[int] = mapped_column(default=ItemState.active)
   wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlist.id"))
   wishlist: Mapped["Wishlist"] = relationship(back_populates="items")