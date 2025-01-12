import pytest
from app import create_app, db


@pytest.fixture
def app():
    wishlist_app = create_app()
    wishlist_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    wishlist_app.config["TESTING"] = True

    with wishlist_app.app_context():
        db.create_all()
        yield wishlist_app
        db.drop_all()


@pytest.fixture
def client(wishlist_app):
    return wishlist_app.test_client()
