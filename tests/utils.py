def create_user(client, username, password):
    return client.post(
        "/register",
        data={"username": username, "password": password, "password_again": password},
    )


def login_user(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def setup_user(client, username, password):
    create_user(client, username, password)


def add_list(client, list_name):
    return client.post("/wishlist", data={"list_name": list_name})
