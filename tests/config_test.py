import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Configure an app instance for testing."""
    wishlist_app = create_app(db_url="sqlite:///:memory:")
    wishlist_app.config["TESTING"] = True

    with wishlist_app.app_context():
        db.create_all()
        yield wishlist_app
        db.drop_all()


@pytest.fixture
def client(wishlist_app):
    """Return a client instance for testing."""
    return wishlist_app.test_client()
