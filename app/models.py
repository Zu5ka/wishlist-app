"""Database"""

from enum import IntEnum
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class ItemState(IntEnum):
    """State of an item."""
    ACTIVE = 0
    RESERVED = 1
    CLAIMED = 2
    DELETED = 3


class ListState(IntEnum):
    """State of a list."""
    ACTIVE = 0
    ARCHIVED = 1
    DELETED = 2


wishlist_shares = db.Table(
    "wishlist_shares",
    db.Column(
        "wishlist_id", db.Integer, db.ForeignKey("wishlist.id"), primary_key=True
    ),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    """User table in databse."""
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    wishlists: Mapped[list["Wishlist"]] = relationship(back_populates="user")

    shared_with_me: Mapped[list["Wishlist"]] = relationship(
        secondary=wishlist_shares, back_populates="shared_with"
    )

    def set_password(self, password: str):
        """Set a new hashed password.

        Keyword arguments:
            password -- The new password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password is correct.

        Keyword arguments:
            password -- The password to check.
        """
        return check_password_hash(self.password_hash, password)

    def search_to_share(self, wishlist, user_query: str) -> list:
        """Return a list of users corresponding to the query.

        Keyword arguments:
            wishlist -- The wishlist on which the user searches.
            user_query -- The search query.
        """
        users = (
            User.query.filter(User.username.ilike("%" + user_query + "%"))
            .limit(20)
            .all()
        )
        return [x for x in users if x not in wishlist.shared_with and x != self]

# third-party library
# pylint: disable=too-few-public-methods
class Wishlist(db.Model):
    """Wishlist table in databse."""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    state: Mapped[int] = mapped_column(default=ListState.ACTIVE)
    items: Mapped[list["Item"]] = relationship(
        back_populates="wishlist", cascade="all, delete-orphan"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="wishlists")

    shared_with: Mapped[list["User"]] = relationship(
        secondary=wishlist_shares, back_populates="shared_with_me"
    )

# third-party library
# pylint: disable=too-few-public-methods
class Item(db.Model):
    """Item table in databse."""
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    state: Mapped[int] = mapped_column(default=ItemState.ACTIVE)
    wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlist.id"))
    wishlist: Mapped["Wishlist"] = relationship(back_populates="items")
