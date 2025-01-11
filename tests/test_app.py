from app.models import Wishlist, User, Item
from .utils import (create_user, login_user, add_list,
                    share_list, logout_user, unshare_list,
                    respond_error, add_item)
from .config_test import app, client

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
    add_list(client, "newlist")
    with app.app_context():
        assert Wishlist.query.filter_by(name="newlist").first() is not None

    response = add_list(client, "   ")
    assert response.text == "Název seznamu musí obsahovat alespoň jeden znak."

    response = add_list(client, "")
    assert response.text == "Název seznamu musí obsahovat alespoň jeden znak."

def test_show_list(client):
    create_user(client, "testuser", "testpass123")
    test_user = User.query.filter_by(username="testuser").first()
    add_list(client, "newlist")
    list = Wishlist.query.filter_by(name="newlist").first()
    response = client.get(f"/wishlist/{list.id}")
    assert response.status_code == 200

    logout_user(client)

    create_user(client, "testuser2", "testpass123")
    response = client.get(f"/wishlist/{list.id}")
    assert response.status_code == 403
    assert response.text == "Nemáte právo zobrazit tento seznam"

    add_list(client, "another_list")
    list = Wishlist.query.filter_by(name="another_list").first()
    response = client.get(f"/wishlist/{list.id}")
    assert response.status_code == 200

    share_list(client, list.id, test_user.id)

    logout_user(client)
    login_user(client, "testuser", "testpass123")

    response = client.get(f"/wishlist/{list.id}")
    assert response.status_code == 200
    
def test_add_item(client):
    create_user(client, "testuser", "testpass123")
    testuser = User.query.filter_by(username="testuser").first()
    add_list(client, "emlist")
    emlist = Wishlist.query.filter_by(name="emlist").first()
    logout_user(client)

    create_user(client, "secuser", "testpass123")
    secuser = User.query.filter_by(username="secuser").first()
    add_list(client, "newlist")
    newlist = Wishlist.query.filter_by(name="newlist").first()

    response = add_item(client, "", newlist.id)
    respond_error(response, 400, "Název položky musí obsahovat alespoň jeden znak.")

    response = add_item(client, "       ", newlist.id)
    respond_error(response, 400, "Název položky musí obsahovat alespoň jeden znak.")

    response = add_item(client, "newitem", emlist.id)
    respond_error(response, 403, "Seznam není Váš.")

    response = add_item(client, "newitem", newlist.id)
    assert response.status_code == 200
    assert Item.query.filter_by(name="newitem").first() is not None

    share_list(client, newlist.id, testuser.id)
    logout_user(client)
    login_user(client, "testuser", "testpass123")

    response = add_item(client, "newitem", newlist.id)
    respond_error(response, 403, "Seznam není Váš.")
    

def test_share_list(client):
    create_user(client, "testuser", "testpass123")
    f_user = User.query.filter_by(username="testuser").first()
    f_user_id = f_user.id
    add_list(client, "some_list")
    f_list = Wishlist.query.filter_by(name="some_list").first()
    f_list_id = f_list.id
    logout_user(client)

    create_user(client, "testuser2", "testpass123")
    s_user = User.query.filter_by(username="testuser2").first()
    s_user_id = s_user.id
    add_list(client, "newlist")
    s_list = Wishlist.query.filter_by(name="newlist").first()
    s_list_id = s_list.id

    response = share_list(client, s_list_id, 55)
    assert response.status_code == 404
    assert response.text == "Uživatel nebo seznam neexistuje."

    response = share_list(client, 55, f_user_id)
    assert response.status_code == 404
    assert response.text == "Uživatel nebo seznam neexistuje."

    response = share_list(client, f_list_id, f_user_id)
    assert response.status_code == 403
    assert response.text == "Seznam patří jinému uživateli."

    response = share_list(client, s_list_id, s_user_id)
    assert response.status_code == 400
    assert response.text == "Nelze nasdílet vlastní seznam."

    response = share_list(client, s_list_id, f_user_id)
    assert response.status_code == 200
    assert f_user in s_list.shared_with

    response = share_list(client, s_list_id, f_user_id)
    assert response.status_code == 400
    assert response.text == "Seznam již je nasdílený."

    logout_user(client)
    login_user(client, "testuser", "testpass123")

    response = share_list(client, s_list_id, s_user_id)
    assert response.status_code == 403
    assert response.text == "Seznam patří jinému uživateli."

def test_unshare_list(client):
    create_user(client, "user_ns", "testpass123")
    user_ns = User.query.filter_by(username="user_ns").first()

    create_user(client, "testuser", "testpass123")
    testuser = User.query.filter_by(username="testuser").first()
    logout_user(client)

    create_user(client, "secuser", "testpass123")
    secuser = User.query.filter_by(username="secuser").first()
    add_list(client, "newlist")
    newlist = Wishlist.query.filter_by(name="newlist").first()
    share_list(client, newlist.id, testuser.id)

    response = unshare_list(client, 55, testuser.id)
    respond_error(response, 404, "Uživatel nebo seznam neexistuje.")
    response = unshare_list(client, newlist.id, 55)
    respond_error(response, 404, "Uživatel nebo seznam neexistuje.")

    response = unshare_list(client, newlist.id, secuser.id)
    respond_error(response, 400, "Nelze provést s vlastním seznamem.")

    response = unshare_list(client, newlist.id, user_ns.id)
    respond_error(response, 400, "Seznam není sdílený s tímto uživatelem.")

    response = unshare_list(client, newlist.id, testuser.id)
    assert response.status_code == 200
    assert "HX-Trigger" in response.headers
    assert not testuser in newlist.shared_with

    share_list(client, newlist.id, testuser.id)

    logout_user(client)
    login_user(client, "testuser", "testpass123")

    response = unshare_list(client, newlist.id, testuser.id)
    respond_error(response, 403, "Seznam patří jinému uživateli.")
