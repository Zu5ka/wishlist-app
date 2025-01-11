from app.models import Wishlist, User
from .utils import create_user, login_user, add_list


def test_register(client):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "testpass123",
            "password_again": "testpass123",
        },
    )
    assert response.status_code == 200
    assert "HX-Redirect" in response.headers
    assert User.query.filter_by(username="testuser").first()

    response = client.post(
        "/register",
        data={"username": "testuser2", "password": "testpass123", "password_again": ""},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Vyplňte všechna pole."

    response = client.post(
        "/register",
        data={"username": "testuser2", "password": "", "password_again": "asdasd"},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Vyplňte všechna pole."

    response = client.post(
        "/register",
        data={"username": "", "password": "testpass123", "password_again": "a"},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Vyplňte všechna pole."

    response = client.post(
        "/register",
        data={"username": "   ", "password": "testpass123", "password_again": "a"},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert (
        response.text
        == "Uživatelské jméno musí obsahovat alespoň 1 znak a heslo musí být dlouhé alespoň 8 znaků."
    )

    response = client.post(
        "/register",
        data={"username": "emptypassword", "password": " ", "password_again": "a"},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert (
        response.text
        == "Uživatelské jméno musí obsahovat alespoň 1 znak a heslo musí být dlouhé alespoň 8 znaků."
    )

    response = client.post(
        "/register",
        data={
            "username": "testuser2",
            "password": "testpass123",
            "password_again": "testnotpass123",
        },
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Hesla se neshodují."

    response = client.post(
        "/register",
        data={"username": "testuser2", "password": "testpass123", "password_again": ""},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Vyplňte všechna pole."

    response = client.post(
        "/register",
        data={"username": "testuser2", "password": "test", "password_again": "test"},
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Zadejte heslo dlouhé alespoň 8 znaků."

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "password": "testpass123",
            "password_again": "testpass123",
        },
    )
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Uživatel s tímto jménem už existuje."

    response = client.post(
        "/register",
        data={
            "username": "testuser2",
            "password": "testpass123",
            "password_again": "testpass123",
        },
    )
    assert response.status_code == 200
    assert "HX-Redirect" in response.headers

    response = client.post(
        "/register",
        data={
            "username": "testuser3",
            "password": "testpass1234",
            "password_again": "testpass1234",
        },
    )
    assert response.status_code == 200
    assert "HX-Redirect" in response.headers


def test_login(client):
    create_user(client, "testuser", "testpass123")

    response = login_user(client, "testuser", "testpass123")
    assert response.status_code == 200
    assert "HX-Redirect" in response.headers

    response = login_user(client, "testuser", "testpass")
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Nesprávné heslo nebo uživatelské jméno."

    response = login_user(client, "notexisting", "testpass123")
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Nesprávné heslo nebo uživatelské jméno."

    response = login_user(client, "", "testpass")
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Zadejte uživatelské jméno i heslo."

    response = login_user(client, "testuser", "")
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Zadejte uživatelské jméno i heslo."

    response = login_user(client, "", "")
    assert response.status_code != 200
    assert "HX-Redirect" not in response.headers
    assert response.text == "Zadejte uživatelské jméno i heslo."


def test_logout(client):
    create_user(client, "test", "testpass123")
    response = client.post("/logout")
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers


def test_add_list(client, app):
    create_user(client, "testuser", "testpass123")
    add_list(client, "new_list")
    with app.app_context():
        assert Wishlist.query.filter_by(name="new_list").first() is not None

    response = add_list(client, "   ")
    assert response.text == "Název seznamu musí obsahovat alespoň jeden znak."

    response = add_list(client, "")
    assert response.text == "Název seznamu musí obsahovat alespoň jeden znak."


def test_show_list(client):
    # TODO
    pass
