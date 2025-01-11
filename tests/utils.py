def create_user(client, username, password):
    return client.post(
        "/register",
        data={"username": username, "password": password, "password_again": password},
    )

def logout_user(client):
    client.post("/logout")

def login_user(client, username, password):
    return client.post("/login", data={"username": username, "password": password})

def setup_user(client, username, password):
    create_user(client, username, password)

def add_list(client, list_name):
    return client.post("/wishlist", data={"list_name": list_name})

def share_list(client, list_id, user_id):
    return client.patch(f"/list/{list_id}/share/{user_id}")

def unshare_list(client, list_id, user_id):
    return client.patch(f"/list/{list_id}/unshare/{user_id}")

def respond_error(response, status, msg):
    assert response.status_code == status
    assert response.text == msg

def add_item(client, item_name, list_id):
    return client.post(f"/{list_id}/item", data={"new_item_name": item_name})
