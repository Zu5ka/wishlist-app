from .utils import create_user, login_user

def test_register(client):
   response = client.post("/register", data={
       "username": "testuser",
       "password": "testpass123",
       "password_again": "testpass123"
   })
   assert response.status_code == 200
   assert "HX-Redirect" in response.headers

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "testpass123",
       "password_again": ""
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Vyplňte všechna pole."

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "",
       "password_again": "asdasd"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Vyplňte všechna pole."

   response = client.post("/register", data={
       "username": "",
       "password": "testpass123",
       "password_again": "a"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Vyplňte všechna pole."

   response = client.post("/register", data={
       "username": "   ",
       "password": "testpass123",
       "password_again": "a"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Uživatelské jméno musí obsahovat alespoň 1 znak a heslo musí být dlouhé alespoň 8 znaků."

   response = client.post("/register", data={
       "username": "emptypassword",
       "password": "",
       "password_again": "a"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Uživatelské jméno musí obsahovat alespoň 1 znak a heslo musí být dlouhé alespoň 8 znaků."

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "testpass123",
       "password_again": "testnotpass123"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Hesla se neshodují."

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "testpass123",
       "password_again": ""
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Hesla se neshodují."

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "test",
       "password_again": "test"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Zadejte heslo dlouhé alespoň 8 znaků."

   response = client.post("/register", data={
       "username": "testuser",
       "password": "testpass123",
       "password_again": "testpass123"
   })
   assert response.status_code != 200
   assert not "HX-Redirect" in response.headers
   assert response.response == "Uživatel s tímto jménem už existuje."

   response = client.post("/register", data={
       "username": "testuser2",
       "password": "testpass123",
       "password_again": "testpass123"
   })
   assert response.status_code == 200
   assert "HX-Redirect" in response.headers

   response = client.post("/register", data={
       "username": "testuser3",
       "password": "testpass1234",
       "password_again": "testpass1234"
   })
   assert response.status_code == 200
   assert "HX-Redirect" in response.headers

def test_login(client):
    create_user(client,"testuser", "testpass123")

    response = login_user(client, "testuser", "testpass123")
    assert response.status_code == 200
    assert "HX-Redirect" in response.headers

    response = login_user(client, "testuser", "testpass")
    assert response.status_code != 200
    assert not "HX-Redirect" in response.headers
    assert response.response == "Nesprávné heslo nebo uživatelské jméno."

    response = login_user(client, "notexisting", "testpass123")
    assert response.status_code != 200
    assert not "HX-Redirect" in response.headers
    assert response.response == "Nesprávné heslo nebo uživatelské jméno."

    response = login_user(client, "","testpass")
    assert response.status_code != 200
    assert not "HX-Redirect" in response.headers
    assert response.response == "Zadejte uživatelské jméno i heslo."

    response = login_user(client, "testuser", "")
    assert response.status_code != 200
    assert not "HX-Redirect" in response.headers
    assert response.response == "Zadejte uživatelské jméno i heslo."

    response = login_user(client, "", "")
    assert response.status_code != 200
    assert not "HX-Redirect" in response.headers
    assert response.response == "Zadejte uživatelské jméno i heslo."

def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers