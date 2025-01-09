from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

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